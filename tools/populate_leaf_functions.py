#!/usr/bin/env python3
"""
Populate units.json with small leaf functions (12-48 bytes) for fast 1.5B/7B workers.
"""

import json
from pathlib import Path
import pefile

IMAGE_PATH = Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe")
UNITS_JSON = Path(r"M:\bl2_decomp\build\units.json")
HEADER_PATH = Path(r"M:\bl2_decomp\include\WillowGame\WillowGame.h")

def populate_leaf_functions(target_count=80):
    pe = pefile.PE(str(IMAGE_PATH), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    text_sec = [s for s in pe.sections if s.Name.strip(b'\x00') == b'.text'][0]
    data = text_sec.get_data()
    text_va = image_base + text_sec.VirtualAddress

    with open(UNITS_JSON, "r") as f:
        manifest = json.load(f)

    existing = set()
    for u in manifest.get("units", []):
        for fn in u.get("functions", []):
            existing.add(fn.get("address").lower())

    discovered = []
    # Scan text section around WillowEngine code
    i = 0x00200000
    end = min(i + 0x00350000, len(data) - 64)

    while i < end and len(discovered) < target_count:
        if data[i:i+3] == b'\x55\x8b\xec':
            for j in range(i + 3, i + 64):
                if data[j] == 0xC3 and j + 1 < len(data) and data[j+1] == 0xCC:
                    fn_len = (j + 1) - i
                    if 12 <= fn_len <= 48:
                        va_str = f"0x{(text_va + i):08X}"
                        if va_str.lower() not in existing:
                            discovered.append({
                                "address": va_str,
                                "name": f"Sub_{va_str[2:]}",
                                "size": fn_len,
                                "matched": False,
                                "signature": f"INT WillowCombatLogic::Sub_{va_str[2:]}(void* thisPtr, INT arg1 = 0, INT arg2 = 0)"
                            })
                            existing.add(va_str.lower())
                            i = j + 1
                    break
        i += 1

    print(f"Discovered {len(discovered)} small leaf functions.")

    # Find or create unit
    combat_unit = None
    for u in manifest["units"]:
        if u["name"] == "WillowEngineCombatLogic":
            combat_unit = u
            break

    if not combat_unit:
        combat_unit = {
            "name": "WillowEngineCombatLogic",
            "source": "src/WillowGame/Combat/WillowCombatLogic.cpp",
            "functions": []
        }
        manifest["units"].append(combat_unit)

    for d in discovered:
        combat_unit["functions"].append(d)

    with open(UNITS_JSON, "w") as f:
        json.dump(manifest, f, indent=2)

    # Now update WillowGame.h with prototypes
    with open(HEADER_PATH, "r") as f:
        header_text = f.read()

    prototypes = []
    for d in discovered:
        prototypes.append(f"    INT {d['name']}(void* thisPtr, INT arg1 = 0, INT arg2 = 0);")

    proto_block = "\n".join(prototypes)
    marker = "namespace WillowCombatLogic\n{"
    if marker in header_text:
        header_text = header_text.replace(marker, f"{marker}\n{proto_block}")
        with open(HEADER_PATH, "w") as f:
            header_text = f.write(header_text)
        print(f"Updated WillowGame.h with {len(discovered)} function prototypes.")

if __name__ == "__main__":
    populate_leaf_functions(80)
