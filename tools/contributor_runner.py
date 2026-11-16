#!/usr/bin/env python3
"""
BL2_DECOMP: Standard Contributor Workflow Runner
Provides an isolated, standard-contributor interface for claiming functions,
inspecting target assembly, compiling locally, and validating byte-match status.

Usage:
    python tools/contributor_runner.py --status
    python tools/contributor_runner.py --next
    python tools/contributor_runner.py --inspect <virtual_address>
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

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


def load_manifest() -> dict:
    manifest_path = Path(__file__).resolve().parent.parent / "build" / "units.json"
    if not manifest_path.exists():
        print(f"Error: {manifest_path} not found.")
        sys.exit(1)
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def show_status(manifest: dict):
    units = manifest.get("units", [])
    total_fns = 0
    matched_fns = 0
    
    print(f"\n{COLOR_BOLD}=== Contributor Work Queue Status ==={COLOR_RESET}")
    for u in units:
        u_name = u.get("name")
        u_fns = u.get("functions", [])
        m_count = sum(1 for f in u_fns if f.get("matched", False))
        total_fns += len(u_fns)
        matched_fns += m_count
        print(f"  Unit: {u_name:<24} | Matched: {m_count}/{len(u_fns)}")
        
    print("-" * 52)
    print(f"Total Progress: {matched_fns}/{total_fns} functions matched.\n")


def claim_next(manifest: dict):
    units = manifest.get("units", [])
    for u in units:
        for fn in u.get("functions", []):
            if not fn.get("matched", False):
                addr = fn.get("address")
                name = fn.get("name")
                size = fn.get("size")
                sig = fn.get("signature")
                source = u.get("source")
                
                print(f"\n{COLOR_BOLD}=== Next Assigned Function ==={COLOR_RESET}")
                print(f"  {COLOR_CYAN}Symbol:{COLOR_RESET}      {name}")
                print(f"  {COLOR_CYAN}Address:{COLOR_RESET}     {addr}")
                print(f"  {COLOR_CYAN}Size:{COLOR_RESET}        {size} bytes")
                print(f"  {COLOR_CYAN}Signature:{COLOR_RESET}   {sig}")
                print(f"  {COLOR_CYAN}File:{COLOR_RESET}        {source}")
                print("-" * 52)
                print(f"Run {COLOR_BOLD}python tools/extract_function.py {addr} --size {size}{COLOR_RESET} to inspect assembly.")
                return
    print(f"{COLOR_GREEN}All registered functions in units.json are matched!{COLOR_RESET}")


def main():
    parser = argparse.ArgumentParser(description="Standard contributor task runner for bl2_decomp.")
    parser.add_argument("--status", action="store_true", help="Display contributor backlog and completed units")
    parser.add_argument("--next", action="store_true", help="Claim and display the next uncompleted function")
    parser.add_argument("--inspect", type=str, help="Inspect target assembly for a function address")
    args = parser.parse_args()

    manifest = load_manifest()

    if args.next:
        claim_next(manifest)
    elif args.inspect:
        subprocess.run([sys.executable, "tools/extract_function.py", args.inspect])
    else:
        show_status(manifest)


if __name__ == "__main__":
    main()
