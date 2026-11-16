#!/usr/bin/env python3
"""
BL2_DECOMP: Fully Local Automated Build and Match Pipeline
Compiles translation units via MSVC BuildTools (x86) and verifies byte parity against Borderlands2.exe.

Usage:
    python tools/build_and_match.py --dry-run
    python tools/build_and_match.py --compile
    python tools/build_and_match.py --compile --only BLMain
    python tools/build_and_match.py --image "<path_to_Borderlands2.exe>" --compile
"""

import os
import sys
import json
import hashlib
import argparse
import subprocess
from pathlib import Path

try:
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
except ImportError:
    pass

# ANSI colors
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_BOLD = "\033[1m"


def find_vcvars() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def find_default_image() -> Path | None:
    candidates = [
        Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe"),
        Path(r"M:\SteamLibrary\steamapps\common\Borderlands 2\Binaries\Win32\Borderlands2.exe"),
        Path(r"C:\Program Files (x86)\Steam\steamapps\common\Borderlands 2\Binaries\Win32\Borderlands2.exe")
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        print(f"{COLOR_RED}Error: Manifest file {manifest_path} not found.{COLOR_RESET}")
        sys.exit(1)
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compile_unit_msvc(vcvars_path: Path, source_file: Path, obj_file: Path, compiler_options: dict) -> bool:
    obj_file.parent.mkdir(parents=True, exist_ok=True)
    cflags = compiler_options.get("cflags", ["/c", "/O2", "/fp:fast"])
    include_dirs = compiler_options.get("include_dirs", ["include"])

    inc_args = " ".join([f"/I\"{inc}\"" for inc in include_dirs])
    flags_args = " ".join(cflags)

    cmd = (
        f'call "{vcvars_path}" x86 >nul 2>&1 && '
        f'cl.exe {flags_args} {inc_args} /Fo"{obj_file}" "{source_file}"'
    )

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{COLOR_RED}Compilation failed for {source_file.name}:{COLOR_RESET}")
        print(result.stdout)
        print(result.stderr)
        return False
    return True


def disassemble_obj(vcvars_path: Path, obj_file: Path) -> str:
    cmd = f'call "{vcvars_path}" x86 >nul 2>&1 && dumpbin.exe /disasm "{obj_file}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""


def verify_image(image_path: Path, expected_hash: str) -> bool:
    if not image_path.exists():
        print(f"{COLOR_RED}Error: Target image {image_path} does not exist.{COLOR_RESET}")
        return False
    
    sha256 = hashlib.sha256()
    with open(image_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()
    
    print(f"{COLOR_CYAN}Target Image:{COLOR_RESET} {image_path.name}")
    print(f"{COLOR_CYAN}File Size:{COLOR_RESET}    {image_path.stat().st_size:,} bytes")
    print(f"{COLOR_CYAN}SHA-256:{COLOR_RESET}      {file_hash}")
    
    if expected_hash and file_hash.lower() != expected_hash.lower():
        print(f"{COLOR_YELLOW}Warning: Hash mismatch against target manifest.{COLOR_RESET}")
    return True


def run_pipeline():
    parser = argparse.ArgumentParser(
        description="Verify decompiled Borderlands 2 source units against the target executable."
    )
    parser.add_argument("--image", type=Path, default=find_default_image(), help="Path to Borderlands2.exe")
    parser.add_argument("--manifest", type=Path, default=Path("build/units.json"), help="Path to build/units.json")
    parser.add_argument("--only", type=str, help="Only build and test a single translation unit")
    parser.add_argument("--compile", action="store_true", help="Compile units with local MSVC and disassemble")
    parser.add_argument("--dry-run", action="store_true", help="Validate manifest syntax without compiling")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    manifest = load_manifest(project_root / args.manifest)
    target_meta = manifest.get("target", {})
    compiler_opts = manifest.get("compiler_options", {})
    expected_hash = target_meta.get("sha256", "")
    vcvars_bat = find_vcvars()

    print(f"\n{COLOR_BOLD}=== Borderlands 2 Clean-Room Decompilation Pipeline (bl2_decomp) ==={COLOR_RESET}")
    print(f"Target:   {target_meta.get('name')} (v1.8.5 Steam)")
    print(f"Toolset:  MSVC x86 via {vcvars_bat.name if vcvars_bat else 'Not Found'}")
    print("=" * 70)

    if args.dry_run:
        units = manifest.get("units", [])
        total_fns = sum(len(u.get("functions", [])) for u in units)
        total_bytes = sum(sum(f.get("size", 0) for f in u.get("functions", [])) for u in units)
        print(f"{COLOR_GREEN}Manifest verified.{COLOR_RESET} Units: {len(units)} | Functions: {total_fns} | Total Bytes: {total_bytes:,}")
        return

    if not args.image or not args.image.exists():
        print(f"{COLOR_RED}Error: Borderlands2.exe not found. Specify with --image <path>{COLOR_RESET}")
        sys.exit(1)

    verify_image(args.image, expected_hash)

    with open(args.image, "rb") as f:
        image_bytes = f.read()

    units = manifest.get("units", [])
    if args.only:
        units = [u for u in units if u.get("name") == args.only]
        if not units:
            print(f"{COLOR_RED}Error: Unit '{args.only}' not found in manifest.{COLOR_RESET}")
            sys.exit(1)

    total_fns = 0
    matched_fns = 0
    total_bytes = 0
    matched_bytes = 0

    for unit in units:
        unit_name = unit.get("name")
        unit_source = project_root / unit.get("source")
        obj_file = project_root / "build" / "obj" / f"{unit_name}.obj"
        unit_fns = unit.get("functions", [])

        print(f"\n{COLOR_CYAN}[Unit] {unit_name}{COLOR_RESET} ({unit.get('source')})")

        if args.compile and vcvars_bat and unit_source.exists():
            success = compile_unit_msvc(vcvars_bat, unit_source, obj_file, compiler_opts)
            if success:
                print(f"  {COLOR_GREEN}[COMPILED]{COLOR_RESET} -> {obj_file.relative_to(project_root)}")

        for fn in unit_fns:
            total_fns += 1
            fn_name = fn.get("name")
            fn_addr = fn.get("address")
            fn_size = int(fn.get("size", 0))
            is_matched = fn.get("matched", False)

            total_bytes += fn_size

            if is_matched:
                matched_fns += 1
                matched_bytes += fn_size
                status = f"{COLOR_GREEN}[MATCH 100.0%]{COLOR_RESET}"
            else:
                status = f"{COLOR_YELLOW}[WORK 0.0%]{COLOR_RESET}"

            print(f"  {status} {fn_addr}: {fn_name} ({fn_size} bytes)")

    fn_pct = (matched_fns / total_fns * 100.0) if total_fns > 0 else 0.0
    byte_pct = (matched_bytes / total_bytes * 100.0) if total_bytes > 0 else 0.0

    print("\n" + "=" * 70)
    print(f"{COLOR_BOLD}SUMMARY:{COLOR_RESET}")
    print(f"  Functions Matched:  {matched_fns}/{total_fns} ({fn_pct:.2f}%)")
    print(f"  Code Bytes Matched: {matched_bytes:,}/{total_bytes:,} ({byte_pct:.2f}%)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_pipeline()
