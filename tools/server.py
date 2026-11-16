#!/usr/bin/env python3
"""
BL2_DECOMP: Master Cluster Task Server
Runs on kharmadesk (port 8080). Serves tasks to local and remote workers (Legion laptop),
verifies byte matches via local MSVC, updates units.json, and commits to git.

Usage:
    python tools/server.py --port 8080
"""

import os
import sys
import json
import time
import struct
import argparse
import subprocess
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
except ImportError:
    pass

COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_BOLD = "\033[1m"


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "build" / "units.json"
ESCALATIONS_PATH = PROJECT_ROOT / "build" / "escalations.json"
ALERT_FLAG_PATH = PROJECT_ROOT / "build" / "escalation_alert.flag"
TARGET_IMAGE = Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe")
VCVARS_BAT = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat")

# Global state
ACTIVE_LEASES = {}  # address -> (worker_id, timestamp)
LEASE_TIMEOUT_SECONDS = 60
FAILURES_BY_ADDR = {}  # address -> {"count": int, "errors": list, "last_code": str, "workers": list, "tier_fails": dict}
FUNCTION_TIERS = {}  # address -> int (1=1.5B, 2=7B, 3=14B, 4=Antigravity)
ESCALATIONS = {}  # address -> dict
MAX_TIER_FAILURES = 20  # 20 attempts per tier before step-up promotion
UNIT_GUIDELINES = {}  # unit_name -> str (pattern guideline applied to all functions in unit)


def get_function_tier(addr: str, size: int) -> int:
    if addr in FUNCTION_TIERS:
        return FUNCTION_TIERS[addr]
    # Default initial tier assignment based on size
    tier = 1 if size <= 48 else 3
    FUNCTION_TIERS[addr] = tier
    return tier


def get_combined_guidelines(unit_name: str, disasm: list, fn_hints: str) -> str:
    """Combines individual function hints, unit guidelines, and opcode pattern guidelines."""
    guidelines = []
    if fn_hints:
        guidelines.append(fn_hints)
    if unit_name in UNIT_GUIDELINES:
        guidelines.append(UNIT_GUIDELINES[unit_name])

    # Pattern check: 32-bit __thiscall member methods
    has_ret4 = any("ret" in i.get("mnemonic", "") and "4" in i.get("op_str", "") for i in disasm)
    has_ecx_this = any("ecx" in i.get("op_str", "") for i in disasm)
    if has_ret4 and has_ecx_this:
        guidelines.append(
            "PATTERN: This function is a 32-bit __thiscall member method taking 1 argument (callee cleanup ret 4). "
            "Register ECX is 'this'. Write standard C++ field assignments (e.g. this->field = arg1) without inline __asm."
        )

    return "\n".join(guidelines)


def save_escalations():
    try:
        with open(ESCALATIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(ESCALATIONS, f, indent=2)
        if ESCALATIONS:
            with open(ALERT_FLAG_PATH, "w", encoding="utf-8") as f:
                f.write(f"ESCALATION_ALERT: {len(ESCALATIONS)} functions flagged at {time.ctime()}\n")
        elif ALERT_FLAG_PATH.exists():
            ALERT_FLAG_PATH.unlink(missing_ok=True)
    except Exception as e:
        print(f"Error saving escalations: {e}")


def load_manifest() -> dict:
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: dict):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def get_function_disassembly(addr_hex: str, size: int) -> list:
    if not TARGET_IMAGE.exists():
        return []
    target_va = int(addr_hex, 16)
    pe = pefile.PE(str(TARGET_IMAGE), fast_load=True)
    rva = target_va - pe.OPTIONAL_HEADER.ImageBase
    try:
        offset = pe.get_offset_from_rva(rva)
        with open(TARGET_IMAGE, "rb") as f:
            f.seek(offset)
            code_bytes = f.read(size)
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        return [{"address": hex(i.address), "bytes": i.bytes.hex(), "mnemonic": i.mnemonic, "op_str": i.op_str} for i in md.disasm(code_bytes, target_va)]
    except Exception as e:
        print(f"Disassembly error for {addr_hex}: {e}")
        return []


def extract_obj_code(obj_path: Path) -> bytes:
    """Extracts raw compiled machine code bytes from MSVC COFF .obj file."""
    if not obj_path.exists():
        return b""
    with open(obj_path, "rb") as f:
        data = f.read()
    if len(data) < 20:
        return b""
    num_sec = struct.unpack("<H", data[2:4])[0]
    for i in range(num_sec):
        hdr = 20 + i * 40
        name = data[hdr:hdr+8].rstrip(b"\x00").decode("latin1", errors="ignore")
        if name in (".text", ".text$mn"):
            size = struct.unpack("<I", data[hdr+16:hdr+20])[0]
            ptr = struct.unpack("<I", data[hdr+20:hdr+24])[0]
            return data[ptr:ptr+size]
    return b""


def test_compile_match(unit_name: str, fn_addr: str, fn_size: int, candidate_code: str) -> tuple[bool, float, str]:
    """Compiles candidate code snippet with local MSVC and compares bytes against target binary."""
    scratch_dir = PROJECT_ROOT / "build" / "scratch"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    
    test_src = scratch_dir / f"test_{fn_addr[2:]}.cpp"
    test_obj = scratch_dir / f"test_{fn_addr[2:]}.obj"

    # Wrap code with necessary headers
    full_source = (
        '#include "Common.h"\n'
        '#include "WillowGame/WillowGame.h"\n\n'
        f'{candidate_code}\n'
    )
    with open(test_src, "w", encoding="utf-8") as f:
        f.write(full_source)

    cmd = (
        f'call "{VCVARS_BAT}" x86 >nul 2>&1 && '
        f'cl.exe /c /O2 /Oi /Ot /Oy /GF /EHsc /MT /fp:fast /wd4996 '
        f'/I"{PROJECT_ROOT / "include"}" /I"{PROJECT_ROOT / "include/Core"}" '
        f'/I"{PROJECT_ROOT / "include/Engine"}" /I"{PROJECT_ROOT / "include/WillowGame"}" '
        f'/Fo"{test_obj}" "{test_src}"'
    )

    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, 0.0, f"Compilation failed:\n{proc.stdout}\n{proc.stderr}"

    # Extract target bytes from Borderlands2.exe
    target_va = int(fn_addr, 16)
    pe = pefile.PE(str(TARGET_IMAGE), fast_load=True)
    rva = target_va - pe.OPTIONAL_HEADER.ImageBase
    offset = pe.get_offset_from_rva(rva)
    with open(TARGET_IMAGE, "rb") as f:
        f.seek(offset)
        target_bytes = f.read(fn_size)

    compiled_code = extract_obj_code(test_obj)
    if not compiled_code:
        return False, 0.0, "Could not extract machine code from compiled object file."

    if compiled_code == target_bytes:
        return True, 100.0, "EXACT 100% BYTE MATCH!"

    common_len = min(len(compiled_code), len(target_bytes))
    matching_bytes = sum(1 for a, b in zip(compiled_code[:common_len], target_bytes[:common_len]) if a == b)
    accuracy = (matching_bytes / max(len(target_bytes), len(compiled_code))) * 100.0
    return False, accuracy, f"Parity mismatch: {matching_bytes}/{len(target_bytes)} bytes match ({accuracy:.1f}%), emitted {len(compiled_code)} bytes vs target {len(target_bytes)} bytes."



class ClusterRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        now = time.time()
        if self.path.startswith("/task"):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            tier_str = params.get("tier", ["1"])[0].lower()
            if tier_str in ("1", "small", "1.5b"):
                w_tier = 1
            elif tier_str in ("2", "mid", "7b", "8b"):
                w_tier = 2
            elif tier_str in ("3", "large", "14b", "32b"):
                w_tier = 3
            else:
                w_tier = 2
            worker_id = params.get("worker_id", ["unknown"])[0]

            manifest = load_manifest()
            units = manifest.get("units", [])
            for u in units:
                unit_name = u.get("name")
                for fn in u.get("functions", []):
                    addr = fn.get("address")
                    size = fn.get("size", 32)
                    if not fn.get("matched", False):
                        fn_tier = get_function_tier(addr, size)

                        # Level 4 is reserved for Antigravity supervisor
                        if fn_tier == 4 and worker_id != "antigravity":
                            continue

                        # Routing checks based on worker tier capability
                        if w_tier == 1 and fn_tier != 1:
                            continue
                        if w_tier == 2 and fn_tier > 2:
                            continue
                        if w_tier == 3 and fn_tier > 3:
                            continue

                        lease = ACTIVE_LEASES.get(addr)
                        if not lease or (now - lease[1] > LEASE_TIMEOUT_SECONDS):
                            ACTIVE_LEASES[addr] = (worker_id, now)
                            disasm = get_function_disassembly(addr, size)
                            prior_errors = FAILURES_BY_ADDR.get(addr, {}).get("errors", [])
                            feedback = "\n".join(prior_errors[-2:]) if prior_errors else ""
                            resp = {
                                "status": "assigned",
                                "unit": unit_name,
                                "source": u.get("source"),
                                "address": addr,
                                "name": fn.get("name"),
                                "size": size,
                                "tier": fn_tier,
                                "signature": fn.get("signature"),
                                "hints": get_combined_guidelines(unit_name, disasm, fn.get("hints", "")),
                                "prior_feedback": feedback,
                                "disassembly": disasm
                            }
                            return self._send_json(200, resp)

            return self._send_json(200, {"status": "empty", "message": "All functions currently completed or leased."})

        elif self.path == "/escalations":
            return self._send_json(200, {
                "count": len(ESCALATIONS),
                "threshold": ESCALATION_THRESHOLD,
                "escalations": ESCALATIONS
            })
        elif self.path.startswith("/release"):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            addr = parse_qs(parsed.query).get("address", [""])[0]
            if addr:
                ACTIVE_LEASES.pop(addr, None)
                return self._send_json(200, {"status": "released", "address": addr})
            return self._send_json(400, {"error": "Missing address"})
        elif self.path == "/setup.ps1":
            setup_script_path = Path(r"C:\MindVault\deploy_agent_bridge.ps1")
            if setup_script_path.exists():
                with open(setup_script_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self._send_json(404, {"error": "Setup script not found"})
        elif self.path == "/status":
            manifest = load_manifest()
            total_fns = 0
            matched_fns = 0
            for u in manifest.get("units", []):
                for f in u.get("functions", []):
                    total_fns += 1
                    if f.get("matched", False):
                        matched_fns += 1
            return self._send_json(200, {
                "server": "bl2_decomp_master",
                "total_functions": total_fns,
                "matched_functions": matched_fns,
                "active_leases": len(ACTIVE_LEASES),
                "escalations": len(ESCALATIONS),
                "target_image": TARGET_IMAGE.name
            })
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/submit":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                return self._send_json(400, {"error": "Invalid JSON"})

            unit_name = data.get("unit")
            fn_addr = data.get("address")
            fn_size = int(data.get("size", 32))
            code = data.get("code")
            worker_id = data.get("worker_id", "unknown")

            print(f"\n{COLOR_CYAN}[Cluster Submission]{COLOR_RESET} {fn_addr} from worker: {worker_id}")

            is_match, match_pct, detail = test_compile_match(unit_name, fn_addr, fn_size, code)
            if is_match and match_pct >= 100.0:
                print(f"  {COLOR_GREEN}[VERIFIED 100% MATCH]{COLOR_RESET} {fn_addr}")
                manifest = load_manifest()
                for u in manifest.get("units", []):
                    for fn in u.get("functions", []):
                        if fn.get("address") == fn_addr:
                            fn["matched"] = True
                save_manifest(manifest)
                ACTIVE_LEASES.pop(fn_addr, None)
                FAILURES_BY_ADDR.pop(fn_addr, None)
                ESCALATIONS.pop(fn_addr, None)
                save_escalations()
                return self._send_json(200, {"status": "accepted", "match_pct": 100.0})
            else:
                print(f"  {COLOR_RED}[REJECTED]{COLOR_RESET} {detail[:120]}")
                ACTIVE_LEASES.pop(fn_addr, None)

                # Record failure & check step-up promotion
                w_tier = int(data.get("worker_tier", 1))
                info = FAILURES_BY_ADDR.setdefault(fn_addr, {"count": 0, "errors": [], "last_code": "", "workers": [], "tier_fails": {1: 0, 2: 0, 3: 0}})
                info["count"] += 1
                if detail not in info["errors"]:
                    info["errors"].append(detail[:250])
                info["last_code"] = code
                if worker_id not in info["workers"]:
                    info["workers"].append(worker_id)
                tier_fails = info.setdefault("tier_fails", {1: 0, 2: 0, 3: 0})
                tier_fails[w_tier] = tier_fails.get(w_tier, 0) + 1

                # Step-Up Escalation Ladder
                cur_tier = get_function_tier(fn_addr, fn_size)
                if cur_tier == 1 and tier_fails.get(1, 0) >= MAX_TIER_FAILURES:
                    FUNCTION_TIERS[fn_addr] = 2
                    print(f"  {COLOR_YELLOW}[STEP-UP ESCALATION]{COLOR_RESET} Function {fn_addr} promoted: Tier 1 (1.5B) -> Tier 2 (7B)")
                elif cur_tier == 2 and tier_fails.get(2, 0) >= MAX_TIER_FAILURES:
                    FUNCTION_TIERS[fn_addr] = 3
                    print(f"  {COLOR_YELLOW}[STEP-UP ESCALATION]{COLOR_RESET} Function {fn_addr} promoted: Tier 2 (7B) -> Tier 3 (14B)")
                elif cur_tier == 3 and tier_fails.get(3, 0) >= MAX_TIER_FAILURES:
                    FUNCTION_TIERS[fn_addr] = 4
                    if fn_addr not in ESCALATIONS:
                        ESCALATIONS[fn_addr] = {
                            "address": fn_addr,
                            "unit": unit_name,
                            "size": fn_size,
                            "failure_count": info["count"],
                            "tier_breakdown": tier_fails,
                            "recent_errors": info["errors"][-3:],
                            "last_code": code,
                            "workers_attempted": info["workers"],
                            "disassembly": get_function_disassembly(fn_addr, fn_size),
                            "escalated_at": time.time()
                        }
                        save_escalations()
                        print(f"  {COLOR_RED}[LEVEL 4 ESCALATION]{COLOR_RESET} Function {fn_addr} exhausted all local models (Tier 1-3). Flagged for Antigravity review.")

                return self._send_json(200, {"status": "rejected", "match_pct": match_pct, "error": detail})

        elif self.path == "/resolve_escalation":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                return self._send_json(400, {"error": "Invalid JSON"})

            fn_addr = data.get("address")
            action = data.get("action", "set_hint")
            hints = data.get("hints", "")
            apply_unit = data.get("apply_to_unit", False)
            target_unit = data.get("unit", "")

            if apply_unit and target_unit:
                UNIT_GUIDELINES[target_unit] = hints
                manifest = load_manifest()
                for u in manifest.get("units", []):
                    if u.get("name") == target_unit:
                        for fn in u.get("functions", []):
                            fn_a = fn.get("address")
                            FAILURES_BY_ADDR.pop(fn_a, None)
                            FUNCTION_TIERS[fn_a] = 1 if fn.get("size", 32) <= 48 else 3
                            ESCALATIONS.pop(fn_a, None)
                save_escalations()
                print(f"  {COLOR_GREEN}[SUPERVISOR APPLIED UNIT-WIDE PATTERN RULE]{COLOR_RESET} Unit '{target_unit}' -> {hints}")
                return self._send_json(200, {"status": "resolved", "action": "set_unit_rule", "unit": target_unit})

            if action == "set_hint":
                manifest = load_manifest()
                for u in manifest.get("units", []):
                    for fn in u.get("functions", []):
                        if fn.get("address") == fn_addr:
                            fn["hints"] = hints
                save_manifest(manifest)
                FAILURES_BY_ADDR.pop(fn_addr, None)
                FUNCTION_TIERS[fn_addr] = 1 if fn.get("size", 32) <= 48 else 3
                ESCALATIONS.pop(fn_addr, None)
                save_escalations()
                print(f"  {COLOR_GREEN}[SUPERVISOR APPLIED HINT]{COLOR_RESET} {fn_addr}: {hints}")
                return self._send_json(200, {"status": "resolved", "action": "set_hint", "address": fn_addr})
            elif action == "reset":
                FAILURES_BY_ADDR.pop(fn_addr, None)
                FUNCTION_TIERS[fn_addr] = 1
                ESCALATIONS.pop(fn_addr, None)
                save_escalations()
                return self._send_json(200, {"status": "resolved", "action": "reset", "address": fn_addr})
            else:
                return self._send_json(400, {"error": f"Unknown action: {action}"})


def main():
    parser = argparse.ArgumentParser(description="Master Task Server for bl2_decomp cluster.")
    parser.add_argument("--port", type=int, default=8080, help="Server port (default: 8080)")
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    server_address = ("0.0.0.0", args.port)
    httpd = HTTPServer(server_address, ClusterRequestHandler)

    print(f"\n{COLOR_BOLD}=== bl2_decomp Master Task Server ==={COLOR_RESET}")
    print(f"Listening: http://0.0.0.0:{args.port}")
    print(f"Image:     {TARGET_IMAGE}")
    print("Ready to serve tasks to local and remote nodes...\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down task server.")
        httpd.server_close()


if __name__ == "__main__":
    main()
