#!/usr/bin/env python3
"""
Fixes all function prototypes in WillowGame.h and build/units.json by accurately
inspecting both stdcall (ret N) and cdecl ([ebp + N] / [esp + N]) argument layouts
from Borderlands2.exe within the exact bounds of each function.
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

# Build lookup of function sizes from manifest
fn_sizes = {}
fn_units = {}
for u in manifest.get("units", []):
    for fn in u.get("functions", []):
        addr_clean = "0x" + fn["address"].upper().replace("0X", "").lstrip("0").zfill(8)
        fn_sizes[addr_clean] = fn.get("size", 32)
        fn_units[addr_clean] = fn

dummy_pattern = re.compile(r"^\s*(?:INT|void|static\s+void\s+__[a-z]+)\s+(Sub_[0-9A-Fa-f]{8})\s*\([^)]*\)\s*;", re.MULTILINE)

fixed_count = 0
updated_manifest_count = 0

with open(TARGET_IMAGE, "rb") as f:
    for match in dummy_pattern.finditer(header_text):
        fn_name = match.group(1)
        addr_raw = fn_name.split("_")[1].upper()
        addr_clean = "0x" + addr_raw.zfill(8)
        va = int(addr_clean, 16)
        fn_size = fn_sizes.get(addr_clean, 32)

        rva = va - pe.OPTIONAL_HEADER.ImageBase
        try:
            offset = pe.get_offset_from_rva(rva)
        except Exception:
            continue

        f.seek(offset)
        code = f.read(fn_size)
        disasm = list(md.disasm(code, va))
        if not disasm:
            continue

        # Check return instruction and calling convention
        ret_bytes = 0
        has_ret = False
        for inst in disasm:
            if inst.mnemonic.startswith("ret"):
                has_ret = True
                if inst.op_str.strip().isdigit():
                    ret_bytes = int(inst.op_str.strip())
                break

        # Check if ecx is used as 'this'
        uses_ecx_this = False
        for inst in disasm[:6]:
            if "ecx" in inst.op_str and inst.mnemonic not in ("xor", "mov") and not inst.op_str.startswith("ecx,"):
                uses_ecx_this = True
                break
            if inst.op_str.startswith("ecx,"):
                break

        # Calculate argument count
        if ret_bytes > 0:
            num_args = ret_bytes // 4
        else:
            # Check highest stack offset read: [ebp + X]
            max_offset = 0
            has_ebp_frame = any(i.mnemonic == "mov" and "ebp, esp" in i.op_str for i in disasm[:3])
            for inst in disasm:
                if has_ebp_frame:
                    m = re.search(r"\[ebp \+ (?:0x([0-9a-fA-F]+)|([0-9]+))\]", inst.op_str)
                    if m:
                        val = int(m.group(1), 16) if m.group(1) else int(m.group(2))
                        if val >= 8 and val > max_offset:
                            max_offset = val
                else:
                    m = re.search(r"\[esp \+ (?:0x([0-9a-fA-F]+)|([0-9]+))\]", inst.op_str)
                    if m:
                        val = int(m.group(1), 16) if m.group(1) else int(m.group(2))
                        if val >= 4 and val > max_offset:
                            max_offset = val + 4 # normalize to ebp frame (+4 for ret addr)
            if max_offset >= 8:
                num_args = (max_offset - 8) // 4 + 1
            else:
                num_args = 0

        # Construct prototype
        if uses_ecx_this:
            # Member method (__thiscall)
            if num_args == 0:
                proto = f"void {fn_name}();"
                manifest_sig = f"void __thiscall WillowCombatLogic::{fn_name}()"
            elif num_args == 1:
                proto = f"void {fn_name}(void* a1);"
                manifest_sig = f"void __thiscall WillowCombatLogic::{fn_name}(void* a1)"
            else:
                args = ", ".join([f"void* a{i+1}" for i in range(num_args)])
                proto = f"void {fn_name}({args});"
                manifest_sig = f"void __thiscall WillowCombatLogic::{fn_name}({args})"
        else:
            call_conv = "__stdcall" if ret_bytes > 0 else "__cdecl"
            if num_args == 0:
                proto = f"static void {call_conv} {fn_name}();"
                manifest_sig = f"void {call_conv} WillowCombatLogic::{fn_name}()"
            elif num_args == 1:
                proto = f"static void {call_conv} {fn_name}(void* a1);"
                manifest_sig = f"void {call_conv} WillowCombatLogic::{fn_name}(void* a1)"
            else:
                args = ", ".join([f"void* a{i+1}" for i in range(num_args)])
                proto = f"static void {call_conv} {fn_name}({args});"
                manifest_sig = f"void {call_conv} WillowCombatLogic::{fn_name}({args})"

        old_line = match.group(0).strip()
        new_line = "    " + proto
        if old_line != proto:
            header_text = header_text.replace(old_line, new_line)
            fixed_count += 1

        # Also update manifest
        if addr_clean in fn_units:
            fn_units[addr_clean]["signature"] = manifest_sig
            updated_manifest_count += 1

with open(HEADER_PATH, "w", encoding="utf-8") as f:
    f.write(header_text)

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Header: Fixed {fixed_count} function declarations in {HEADER_PATH.name}")
print(f"Manifest: Updated {updated_manifest_count} signatures in {MANIFEST_PATH.name}")
