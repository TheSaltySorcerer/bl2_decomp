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
import argparse
from urllib import request, error

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


def run_worker():
    parser = argparse.ArgumentParser(description="Remote Worker Node for bl2_decomp cluster.")
    parser.add_argument("--server", type=str, default="http://100.103.169.13:8080", help="Master server URL")
    parser.add_argument("--llm", type=str, default="http://127.0.0.1:11434/v1", help="Local LLM endpoint")
    parser.add_argument("--model", type=str, default="qwen2.5-coder:7b", help="Model name in local runtime")
    parser.add_argument("--worker-id", type=str, default="legion_rtx5060", help="Worker node identifier")
    parser.add_argument("--tier", type=str, default="", help="Worker tier: 'small' (<=48 bytes) or 'large' (>48 bytes)")
    args = parser.parse_args()

    tier = args.tier
    model_lower = args.model.lower()
    if "1.5b" in model_lower:
        num_tier = 1
    elif any(k in model_lower for k in ["7b", "8b"]):
        num_tier = 2
    else:
        num_tier = 3

    if not tier:
        tier = str(num_tier)

    print(f"\n{COLOR_BOLD}=== bl2_decomp Remote Worker Node ({args.worker_id}) ==={COLOR_RESET}")
    print(f"Master Server: {args.server}")
    print(f"Local LLM:     {args.llm} ({args.model})")
    print(f"Routing Tier:  Tier {num_tier} (1=1.5B scout, 2=7B mid, 3=14B/32B heavy)")
    print("=" * 66)

    while True:
        try:
            req = request.Request(f"{args.server}/task?worker_id={args.worker_id}&tier={num_tier}")
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

        prompt = (
            f"Target Function: {fn_name}\n"
            f"Virtual Address: {addr}\n"
            f"Size: {size} bytes\n"
            f"Signature: {sig}\n"
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
                "worker_id": args.worker_id,
                "worker_tier": num_tier
            }

            sub_data = json.dumps(submit_payload).encode("utf-8")
            sub_req = request.Request(f"{args.server}/submit", data=sub_data, headers={"Content-Type": "application/json"})

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
