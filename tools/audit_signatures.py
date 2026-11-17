#!/usr/bin/env python3
import json
import re
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

md = Cs(CS_ARCH_X86, CS_MODE_32)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_IMAGE = Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe")
MANIFEST_PATH = PROJECT_ROOT / "build" / "units.json"
HEADER_PATH = PROJECT_ROOT / "include" / "WillowGame" / "WillowGame.h"

pe = pefile.PE(str(TARGET_IMAGE), fast_load=True)
manifest = json.load(open(MANIFEST_PATH))
header_text = open(HEADER_PATH).read()

results = []
with open(TARGET_IMAGE, "rb") as f:
    for u in manifest.get("units", []):
        unit_name = u.get("name")
        for fn in u.get("functions", []):
            addr_str = fn.get("address")
            va = int(addr_str, 16)
            size = fn.get("size", 32)
            rva = va - pe.OPTIONAL_HEADER.ImageBase
            offset = pe.get_offset_from_rva(rva)
            f.seek(offset)
            code = f.read(size)

            disasm = list(md.disasm(code, va))
            if not disasm:
                continue

            # Check return instruction
            ret_bytes = 0
            has_ret = False
            for inst in disasm:
                if inst.mnemonic.startswith("ret"):
                    has_ret = True
                    if inst.op_str.strip().isdigit():
                        ret_bytes = int(inst.op_str.strip())
                    break

            # Check if ecx is used before being overwritten
            uses_ecx_this = False
            for inst in disasm[:6]:
                if "ecx" in inst.op_str and inst.mnemonic not in ("xor", "mov") and not inst.op_str.startswith("ecx,"):
                    uses_ecx_this = True
                    break
                if inst.op_str.startswith("ecx,"):
                    break

            # Find declaration in header
            fn_base_name = fn.get("name", "").split("::")[-1]
            header_match = re.search(r"([^\n;]+?" + re.escape(fn_base_name) + r"\s*\([^;]*\)\s*;)", header_text)
            header_decl = header_match.group(1).strip() if header_match else "NOT_DECLARED"

            # Expected stack args based on ret_bytes
            expected_stack_args = ret_bytes // 4

            results.append({
                "unit": unit_name,
                "address": addr_str,
                "name": fn_base_name,
                "size": size,
                "ret_bytes": ret_bytes,
                "expected_stack_args": expected_stack_args,
                "uses_ecx": uses_ecx_this,
                "header_decl": header_decl,
                "disasm": disasm
            })

print(f"Total functions analyzed: {len(results)}")
discrepancies = []
for r in results:
    decl = r["header_decl"]
    # Check if param count in declaration matches expected_stack_args
    if decl != "NOT_DECLARED":
        # Extract params inside parentheses
        params_str = decl[decl.find("(")+1:decl.rfind(")")]
        param_list = [p.strip() for p in params_str.split(",") if p.strip() and p.strip() != "void"]
        decl_param_count = len(param_list)

        # If it's a non-static member method (__thiscall), this is in ECX, so stack params = decl_param_count
        # If it had void* thisPtr as a param, that was a fake placeholder!
        has_fake_this = any("thisptr" in p.lower() for p in param_list)
        if has_fake_this or (decl_param_count != r["expected_stack_args"] and not (r["uses_ecx"] and decl_param_count == r["expected_stack_args"])):
            discrepancies.append((r, decl, decl_param_count))

print(f"\nFound {len(discrepancies)} header declaration discrepancies:")
for r, decl, count in discrepancies:
    print(f"  [{r['address']}] {r['name']} (size {r['size']}): ret {r['ret_bytes']} ({r['expected_stack_args']} stack args), ecx={r['uses_ecx']}")
    print(f"    Current header: {decl}")
