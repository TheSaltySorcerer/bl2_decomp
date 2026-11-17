#!/usr/bin/env python3
"""
BL2_DECOMP: Remote Cluster Worker Node
Designed to run on satellite nodes (e.g. Legion laptop, Kara's rig, ThinkPad).
Pulls tasks from kharmadesk master server, prompts local GPU (Ollama / LM Studio),
and submits candidate C++ to the master for MSVC byte-parity verification.

Usage:
    python tools/remote_worker.py --server "http://100.103.169.13:8080" --model "qwen2.5-coder:7b"
"""

import os
import sys
import time
import json
import socket
import argparse
from pathlib import Path
from urllib import request, error

try:
    import ctypes
    import ctypes.wintypes
except ImportError:
    ctypes = None

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_BOLD = "\033[1m"


SYSTEM_PROMPT = """You are an expert Unreal Engine 3 / WillowEngine reverse engineer matching x86 machine code for Borderlands 2 (Borderlands2.exe) using MSVC (cl.exe /O2 /Oi /Ot /Oy- /GF /EHsc /MT /fp:fast).
MANDATORY REVERSE-ENGINEERING GUIDELINES:
1. DO NOT use SSE/AVX intrinsics (_mm_loadu_ps, __m128) or inline assembly (__asm). Gearbox developers wrote clean, standard C++. MSVC's optimizer auto-vectorizes struct/vector copies into movups/movaps. Write standard C++ variable assignments.
2. NEVER invent undeclared variable names like 'station', 'Health', or 'Location'. Only use variables that exist in the function signature, class definition, or parameters.
3. In 32-bit x86 __thiscall methods, register ECX holds the 'this' pointer. Member variable offsets like [ecx+0x50] or [ecx+0x1A4] correspond to class member fields.
4. Direct Memory/Offset Access: If the assembly accesses an offset on a pointer that is not a named struct field (e.g. [esi + 0x448]), access it directly via pointer arithmetic or casting, e.g. *reinterpret_cast<DWORD*>((BYTE*)ptr + 0x448) |= 0x40000;
5. Sub-Function Calls: If the assembly executes 'call <hex_addr>' (e.g. call 0x6fb980), do NOT invent fake function names. Invoke it via typed function pointer: reinterpret_cast<void(__cdecl*)(void*, int)>(0x6fb980)(arg1, arg2);
6. DO NOT redeclare existing types, structs, or enums (FVector, FRotator, FName, FHitResult, AActor, etc.). They are already included in Common.h and WillowGame.h.
7. Output ONLY the raw C++ function implementation inside a single markdown code block (```cpp ... ```). Do NOT include conversational filler."""


def query_local_llm(endpoint: str, model: str, prompt: str) -> str:
    url = f"{endpoint.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 1024
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"{COLOR_RED}Local LLM Error: {e}{COLOR_RESET}")
        return ""


def clean_code_block(raw_text: str) -> str:
    if "```cpp" in raw_text:
        return raw_text.split("```cpp")[1].split("```")[0].strip()
    elif "```" in raw_text:
        return raw_text.split("```")[1].split("```")[0].strip()
    return raw_text.strip()


def discover_master_server() -> str:
    """Attempts to discover the bl2_decomp master server via UDP broadcast, falling back to household LAN IPs."""
    print(f"{COLOR_CYAN}[Discovery] Scanning local network for bl2_decomp master server...{COLOR_RESET}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(1.5)
    for port in [8088, 8081]:
        try:
            sock.sendto(b"BL2_DECOMP_DISCOVER", ("255.255.255.255", port))
            data, _ = sock.recvfrom(1024)
            info = json.loads(data.decode("utf-8"))
            if "server_url" in info:
                print(f"  {COLOR_GREEN}[Discovered via UDP]{COLOR_RESET} {info['server_url']}")
                return info["server_url"]
        except Exception:
            pass

    # Direct household fallback checks
    candidates = [
        "http://172.16.77.10:8080",      # Kharmadesk LAN
        "http://100.103.169.13:8080",     # Kharmadesk Tailscale
        "http://localhost:8080",          # Local
        "http://172.19.197.1:8080",       # WSL host vEthernet
    ]
    for url in candidates:
        try:
            req = request.Request(f"{url}/status", headers={"User-Agent": "BL2WorkerDiscovery"})
            with request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    print(f"  {COLOR_GREEN}[Discovered via LAN Probe]{COLOR_RESET} {url}")
                    return url
        except Exception:
            continue
    return ""


def benchmark_local_model(llm_endpoint: str, model_name: str) -> float:
    """Runs a 30-token test generation to measure real inference speed."""
    print(f"{COLOR_CYAN}[Benchmark] Measuring local tokens/sec for model '{model_name}'...{COLOR_RESET}")
    t0 = time.time()
    url = f"{llm_endpoint.rstrip('/')}/chat/completions"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": "Write one line of C++ code defining a 3D float vector struct."}],
        "temperature": 0.1,
        "max_tokens": 30
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=45) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            elapsed = max(0.05, time.time() - t0)
            tokens = body.get("usage", {}).get("total_tokens", 25)
            tok_s = round(tokens / elapsed, 2)
            print(f"  {COLOR_GREEN}[Benchmark Result]{COLOR_RESET} {tok_s} tok/s ({tokens} tokens in {elapsed:.2f}s)")
            return tok_s
    except Exception as e:
        print(f"  {COLOR_YELLOW}[Benchmark Skipped]{COLOR_RESET} Local test failed ({e}), using default tier estimation.")
        return 0.0


def register_worker_with_master(server_url: str, worker_id: str, model: str, tok_s: float, hardware: str = "") -> dict:
    url = f"{server_url.rstrip('/')}/register_worker"
    payload = {
        "worker_id": worker_id,
        "model": model,
        "benchmark_tok_s": tok_s,
        "hardware": hardware or socket.gethostname()
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"{COLOR_YELLOW}[Register Warning]{COLOR_RESET} Could not register with master: {e}")
        return {}


COMMON_GAME_EXES = {
    "borderlands2.exe", "borderlands3.exe", "borderlands4.exe", "wonderlands.exe",
    "r5apex.exe", "cs2.exe", "dota2.exe", "overwatch.exe", "cod.exe",
    "warframe.x64.exe", "cyberpunk2077.exe", "starfield.exe", "eldenring.exe",
    "helldivers2.exe", "valorant.exe", "destiny2.exe", "gtav.exe", "rdr2.exe",
    "fallout4.exe", "skyrimse.exe", "witcher3.exe"
}


def set_low_process_priority():
    """Sets process priority to BELOW_NORMAL on Windows or nice(10) on Linux so games take precedence."""
    try:
        if sys.platform == "win32" and ctypes:
            k32 = ctypes.windll.kernel32
            k32.GetCurrentProcess.restype = ctypes.c_void_p
            k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
            k32.SetPriorityClass.restype = ctypes.c_bool
            # 0x00004000 = BELOW_NORMAL_PRIORITY_CLASS
            k32.SetPriorityClass(k32.GetCurrentProcess(), 0x00004000)
        elif hasattr(os, "nice"):
            os.nice(10)
    except Exception:
        pass


def detect_active_game() -> str:
    """Scans running processes for active games or heavy 3D shipping binaries."""
    if sys.platform != "win32" or not ctypes:
        return ""
    try:
        TH32CS_SNAPPROCESS = 0x00000002
        k32 = ctypes.windll.kernel32
        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ('dwSize', ctypes.wintypes.DWORD),
                ('cntUsage', ctypes.wintypes.DWORD),
                ('th32ProcessID', ctypes.wintypes.DWORD),
                ('th32DefaultHeapID', ctypes.c_size_t),
                ('th32ModuleID', ctypes.wintypes.DWORD),
                ('cntThreads', ctypes.wintypes.DWORD),
                ('th32ParentProcessID', ctypes.wintypes.DWORD),
                ('pcPriClassBase', ctypes.c_long),
                ('dwFlags', ctypes.wintypes.DWORD),
                ('szExeFile', ctypes.c_char * 260)
            ]
        k32.CreateToolhelp32Snapshot.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
        k32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
        snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if not snap or snap == -1:
            return ""
        entry = PROCESSENTRY32()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
        success = k32.Process32First(snap, ctypes.byref(entry))
        detected = ""
        while success:
            exe = entry.szExeFile.decode('ansi', errors='ignore').lower()
            if exe in COMMON_GAME_EXES or (exe.endswith("-shipping.exe") and not exe.startswith("bl2_")) or (exe.startswith("game") and "gemini" not in exe):
                detected = exe
                break
            success = k32.Process32Next(snap, ctypes.byref(entry))
        k32.CloseHandle(snap)
        return detected
    except Exception:
        return ""


def is_paused_by_user() -> bool:
    """Checks for explicit local pause flag file (~/.bl2_pause or M:\\bl2_decomp\\build\\PAUSE)."""
    p1 = Path(os.environ.get("USERPROFILE", "")) / ".bl2_pause"
    p2 = Path(r"M:\bl2_decomp\build\PAUSE")
    return p1.exists() or p2.exists()


def run_worker():
    parser = argparse.ArgumentParser(description="Remote Worker Node for bl2_decomp cluster.")
    parser.add_argument("--server", type=str, default="", help="Master server URL (leave empty for auto-discovery)")
    parser.add_argument("--llm", type=str, default="http://127.0.0.1:11434/v1", help="Local LLM endpoint")
    parser.add_argument("--model", type=str, default="qwen2.5-coder:7b", help="Model name in local runtime")
    parser.add_argument("--worker-id", type=str, default="", help="Worker node identifier")
    parser.add_argument("--tier", type=str, default="", help="Worker tier override: '1', '2', '3'")
    parser.add_argument("--auto", action="store_true", help="Enable automatic discovery and self-calibration")
    args = parser.parse_args()

    # Subordinate worker thread priority so OS prioritizes games and foreground tasks
    set_low_process_priority()

    # Determine server URL
    server_url = args.server
    if not server_url or args.auto:
        discovered = discover_master_server()
        if discovered:
            server_url = discovered
        elif not server_url:
            server_url = "http://172.16.77.10:8080"

    worker_id = args.worker_id or socket.gethostname().lower()

    # Local benchmark and cluster auto-registration
    tok_s = benchmark_local_model(args.llm, args.model)
    reg_info = register_worker_with_master(server_url, worker_id, args.model, tok_s)

    assigned_tier = reg_info.get("tier")
    if args.tier:
        t_str = args.tier.lower()
        if "1.5b" in t_str or t_str in ("1", "small"):
            num_tier = 1
        elif any(k in t_str for k in ["7b", "8b", "2", "mid"]):
            num_tier = 2
        else:
            num_tier = 3
    elif assigned_tier:
        num_tier = int(assigned_tier)
    else:
        model_lower = args.model.lower()
        if "1.5b" in model_lower:
            num_tier = 1
        elif any(k in model_lower for k in ["7b", "8b"]):
            num_tier = 2
        else:
            num_tier = 3

    attempt_budget = reg_info.get("attempt_budget_5m", 150)

    print(f"\n{COLOR_BOLD}=== bl2_decomp Cluster Worker Node ({worker_id}) ==={COLOR_RESET}")
    print(f"Master Server:   {server_url}")
    print(f"Local LLM:       {args.llm} ({args.model})")
    print(f"Inference Speed: {tok_s} tok/s")
    print(f"Assigned Tier:   Tier {num_tier} (1=1.5B scout, 2=7B mid, 3=14B/32B heavy)")
    print(f"5-Min Budget:    ~{attempt_budget} attempts")
    print("=" * 66)

    while True:
        # Gaming shield & user pause detection: yield immediately if game is active
        active_game = detect_active_game()
        if active_game or is_paused_by_user():
            reason = f"Active game '{active_game}' detected" if active_game else "Pause flag active"
            print(f"{COLOR_YELLOW}[Gaming Shield Active] {reason}. Yielding compute. Sleeping 15s...{COLOR_RESET}")
            time.sleep(15)
            continue
        try:
            req = request.Request(f"{server_url}/task?worker_id={worker_id}&tier={num_tier}")
            with request.urlopen(req, timeout=10) as resp:
                task = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"{COLOR_YELLOW}[Warning] Master server unreachable: {e}. Retrying in 10s...{COLOR_RESET}")
            time.sleep(10)
            continue

        if task.get("status") != "assigned":
            print(f"{COLOR_CYAN}[Idle] No tasks available for tier '{num_tier}'. Sleeping 10s...{COLOR_RESET}")
            time.sleep(10)
            continue

        addr = task.get("address")
        fn_name = task.get("name")
        size = task.get("size")
        sig = task.get("signature")
        unit = task.get("unit")
        fn_tier = task.get("tier", num_tier)
        disasm_list = task.get("disassembly", [])

        print(f"\n{COLOR_BOLD}[Task Received]{COLOR_RESET} {addr} ({fn_name}) | {size} bytes | Tier: {fn_tier} | Unit: {unit}")

        disasm_text = "\n".join([f"  {i['address']}:  {i['bytes']:12s}  {i['mnemonic']:8s} {i['op_str']}" for i in disasm_list])
        hints = task.get("hints")
        hint_text = f"\n[SUPERVISOR ARCHITECTURAL GUIDELINE]:\n{hints}\n" if hints else ""
        prior_fb = task.get("prior_feedback")
        fb_text = f"\n[PRIOR COMPILER / TIER FEEDBACK]:\n{prior_fb}\n" if prior_fb else ""

        seed_code = task.get("seed_code", "")
        seed_pct = float(task.get("seed_pct", 0.0))
        guardrail = task.get("tactical_guardrail", "")
        adv_warning = task.get("adversarial_warning", "")

        seed_section = ""
        if seed_code:
            if seed_pct >= 100.0:
                seed_section = f"\n[VERIFIED ARCHETYPE SIBLING TEMPLATE - ADAPT THIS WORKING CODE]:\n```cpp\n{seed_code}\n```\n"
            else:
                seed_section = f"\n[HIGH-WATER DRAFT ({seed_pct}% ACCURACY) - REFINE THIS BASE]:\n```cpp\n{seed_code}\n```\n"

        guardrail_section = f"\n[TACTICAL COMPILER GUARDRAIL]:\n{guardrail}\n" if guardrail else ""
        adv_section = f"\n[SUPERVISOR ADVERSARIAL ALERT]:\n{adv_warning}\n" if adv_warning else ""

        prompt = (
            f"Target Function: {fn_name}\n"
            f"Virtual Address: {addr}\n"
            f"Size: {size} bytes\n"
            f"Signature: {sig}\n"
            f"{adv_section}"
            f"{seed_section}"
            f"{guardrail_section}"
            f"{hint_text}"
            f"{fb_text}\n"
            f"x86 Disassembly from Borderlands2.exe:\n"
            f"{disasm_text}\n\n"
            f"Please generate the C++ function implementation matching this assembly."
        )

        current_prompt = prompt
        for attempt in range(1, 6):
            print(f"  -> Generating candidate C++ (Attempt {attempt}/5)...")
            raw_response = query_local_llm(args.llm, args.model, current_prompt)
            candidate_code = clean_code_block(raw_response)

            if not candidate_code:
                print(f"  {COLOR_RED}[Error] Empty response from local LLM.{COLOR_RESET}")
                time.sleep(2)
                continue

            submit_payload = {
                "unit": unit,
                "address": addr,
                "size": size,
                "code": candidate_code,
                "worker_id": worker_id,
                "worker_tier": num_tier
            }

            sub_data = json.dumps(submit_payload).encode("utf-8")
            sub_req = request.Request(f"{server_url}/submit", data=sub_data, headers={"Content-Type": "application/json"})

            try:
                with request.urlopen(sub_req, timeout=15) as s_resp:
                    result = json.loads(s_resp.read().decode("utf-8"))
            except Exception as e:
                print(f"  {COLOR_RED}[Error] Failed to submit to master: {e}{COLOR_RESET}")
                break

            if result.get("status") == "accepted":
                print(f"  {COLOR_GREEN}[SUCCESS] Function {addr} matched 100% and accepted by master!{COLOR_RESET}")
                break
            else:
                err = result.get("error", "Byte mismatch")
                print(f"  {COLOR_YELLOW}[Retry] Submission rejected: {err[:90]}...{COLOR_RESET}")
                current_prompt = (
                    f"{prompt}\n\n"
                    f"[PREVIOUS ATTEMPT {attempt} FAILED WITH MSVC FEEDBACK]:\n"
                    f"{err}\n\n"
                    f"Adjust your code: fix any compiler errors, do NOT use SIMD intrinsics or redefine types, and match the target assembly bytes."
                )
                time.sleep(2)

        time.sleep(2)


if __name__ == "__main__":
    run_worker()
