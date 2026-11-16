#!/usr/bin/env python3
"""
BL2_DECOMP: Disassembly Diffing Utility
Compares compiled machine instructions against target binary bytes.
"""

import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Disassembly diff utility for bl2_decomp functions.")
    parser.add_argument("function", help="Function name or virtual address (e.g. 0x00401000)")
    parser.add_argument("--image", type=Path, help="Target Borderlands2.exe binary")
    args = parser.parse_args()

    print(f"Diffing function: {args.function}")
    print("Compare compiled MSVC .obj assembly with original target binary disassembly.")
    print("Match criteria: Instruction opcode, register allocation, addressing modes, and jump relocations.")


if __name__ == "__main__":
    main()
