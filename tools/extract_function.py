#!/usr/bin/env python3
"""
BL2_DECOMP: Function Extractor & Disassembler
Extracts binary opcodes and formats clean assembly and C++ templates from Borderlands2.exe.

Usage:
    python tools/extract_function.py <virtual_address> [--size <bytes>] [--image <path>]
    python tools/extract_function.py 0x014b709a --size 32
"""

import sys
import argparse
from pathlib import Path

try:
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
except ImportError:
    print("Error: Missing required packages. Please install via: pip install pefile capstone")
    sys.exit(1)


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


def extract(addr_str: str, size: int, image_path: Path):
    if not image_path.exists():
        print(f"Error: Target image {image_path} not found.")
        sys.exit(1)

    target_va = int(addr_str, 16) if addr_str.startswith("0x") or addr_str.startswith("0X") else int(addr_str, 10)

    pe = pefile.PE(str(image_path), fast_load=True)
    base_addr = pe.OPTIONAL_HEADER.ImageBase
    target_rva = target_va - base_addr

    try:
        file_offset = pe.get_offset_from_rva(target_rva)
    except Exception as e:
        print(f"Error: Virtual Address {hex(target_va)} (RVA {hex(target_rva)}) is out of bounds: {e}")
        sys.exit(1)

    with open(image_path, "rb") as f:
        f.seek(file_offset)
        code_bytes = f.read(size)

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = list(md.disasm(code_bytes, target_va))

    print("=" * 72)
    print(f" TARGET FUNCTION EXTRACTION: {hex(target_va)}")
    print(f" File: {image_path.name} | Base: {hex(base_addr)} | RVA: {hex(target_rva)} | File Offset: {hex(file_offset)}")
    print("=" * 72)

    print("\n[Target x86 Disassembly]")
    for insn in instructions:
        raw_hex = insn.bytes.hex()
        print(f"  {hex(insn.address)}:  {raw_hex:16s}  {insn.mnemonic:8s} {insn.op_str}")

    print("\n" + "-" * 72)
    print("[C++ Function Template]")
    print(f"// {hex(target_va)} - Length: {size} bytes")
    print(f'DECOMP_FUNCTION("{hex(target_va)}", {size})')
    print(f"void FUN_{hex(target_va)[2:]}()")
    print("{\n    // Match the instructions above\n}\n")

    print("-" * 72)
    print("[Manifest units.json Entry]")
    print("{\n"
          f'  "address": "{hex(target_va)}",\n'
          f'  "name": "FUN_{hex(target_va)[2:]}",\n'
          f'  "size": {size},\n'
          '  "matched": false,\n'
          f'  "signature": "void FUN_{hex(target_va)[2:]}()"\n'
          "}")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Extract function disassembly and generate C++ decomp templates.")
    parser.add_argument("address", help="Virtual Address of function (e.g. 0x00401000 or 0x014b709a)")
    parser.add_argument("--size", type=int, default=64, help="Byte size of function to inspect (default: 64)")
    parser.add_argument("--image", type=Path, default=find_default_image(), help="Path to Borderlands2.exe")
    args = parser.parse_args()

    if not args.image:
        print("Error: Could not locate Borderlands2.exe. Please specify with --image <path>")
        sys.exit(1)

    extract(args.address, args.size, args.image)


if __name__ == "__main__":
    main()
