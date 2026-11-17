#!/usr/bin/env python3
"""
Fixes all 115 copy-pasted dummy prototypes in WillowGame.h by reading
the actual binary return instructions (ret 0, ret 4, ret 8) and ECX register usage
from Borderlands2.exe.
"""

import re
import json
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

md = Cs(CS_ARCH_X86, CS_MODE_32)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_IMAGE = Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe")
HEADER_PATH = PROJECT_ROOT / "include" / "WillowGame" / "WillowGame.h"

MANIFEST_PATH = PROJECT_ROOT / "build" / "units.json"
pe = pefile.PE(str(TARGET_IMAGE), fast_load=True)
manifest = json.load(open(MANIFEST_PATH))
header_text = open(HEADER_PATH).read()

# Find all Sub_xxxx lines in header
dummy_pattern = re.compile(r"^\s*(?:INT|void|static\s+void\s+__[a-z]+)\s+(Sub_[0-9A-Fa-f]{8})\s*\([^)]*\)\s*;", re.MULTILINE)

fn_sizes = {fn["address"].upper(): fn.get("size", 128) for u in manifest.get("units", []) for fn in u.get("functions", [])}

fixed_count = 0
for match in dummy_pattern.finditer(header_text):
    fn_name = match.group(1)
    addr_hex = "0x00" + fn_name.split("_")[1].upper()
    va = int(addr_hex, 16)
    fn_size = fn_sizes.get(addr_hex, 128)
    
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    try:
        offset = pe.get_offset_from_rva(rva)
    except Exception:
        continue

    with open(TARGET_IMAGE, "rb") as f:
        f.seek(offset)
        code = f.read(fn_size)

    disasm = list(md.disasm(code, va))
    if not disasm:
        continue

    # Determine ret opcode
    ret_bytes = 0
    has_ret = False
    for inst in disasm:
        if inst.mnemonic.startswith("ret"):
            has_ret = True
            if inst.op_str.strip().isdigit():
                ret_bytes = int(inst.op_str.strip())
            break

    # Determine if ecx is used as 'this'
    uses_ecx_this = False
    for inst in disasm[:6]:
        if "ecx" in inst.op_str and inst.mnemonic not in ("xor", "mov") and not inst.op_str.startswith("ecx,"):
            uses_ecx_this = True
            break
        if inst.op_str.startswith("ecx,"):
            break

    num_stack_args = ret_bytes // 4

    # Build real C++ prototype
    if uses_ecx_this:
        # Non-static member method (__thiscall in 32-bit MSVC)
        if num_stack_args == 0:
            proto = f"void {fn_name}();"
        elif num_stack_args == 1:
            proto = f"void {fn_name}(void* a1);"
        elif num_stack_args == 2:
            proto = f"void {fn_name}(void* a1, void* a2);"
        else:
            args = ", ".join([f"void* a{i+1}" for i in range(num_stack_args)])
            proto = f"void {fn_name}({args});"
    else:
        # Static helper method (__stdcall if ret N > 0, __cdecl if ret 0)
        call_conv = "__stdcall" if ret_bytes > 0 else "__cdecl"
        if num_stack_args == 0:
            proto = f"static void {call_conv} {fn_name}();"
        elif num_stack_args == 1:
            proto = f"static void {call_conv} {fn_name}(void* a1);"
        elif num_stack_args == 2:
            proto = f"static void {call_conv} {fn_name}(void* a1, void* a2);"
        else:
            args = ", ".join([f"void* a{i+1}" for i in range(num_stack_args)])
            proto = f"static void {call_conv} {fn_name}({args});"

    # Replace dummy line in header
    old_line = match.group(0).strip()
    header_text = header_text.replace(old_line, "    " + proto)
    fixed_count += 1

with open(HEADER_PATH, "w", encoding="utf-8") as f:
    f.write(header_text)

print(f"Successfully fixed {fixed_count} function prototypes in {HEADER_PATH.name}!")
