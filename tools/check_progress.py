#!/usr/bin/env python3
"""
BL2_DECOMP: Progress Tracking Tool
Calculates function matching statistics and formats shields.io badges.
"""

import sys
import json
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent.parent
    manifest_path = project_root / "build" / "units.json"
    
    if not manifest_path.exists():
        print(f"Error: {manifest_path} not found.")
        sys.exit(1)
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    units = data.get("units", [])
    total_fns = 0
    matched_fns = 0
    total_bytes = 0
    matched_bytes = 0
    
    for u in units:
        for fn in u.get("functions", []):
            total_fns += 1
            size = fn.get("size", 0)
            total_bytes += size
            if fn.get("matched", False):
                matched_fns += 1
                matched_bytes += size
                
    fn_pct = (matched_fns / total_fns * 100.0) if total_fns > 0 else 0.0
    byte_pct = (matched_bytes / total_bytes * 100.0) if total_bytes > 0 else 0.0
    
    progress = {
        "target": data.get("target", {}).get("name", "Borderlands2.exe"),
        "total_functions": total_fns,
        "matched_functions": matched_fns,
        "function_percentage": round(fn_pct, 2),
        "total_bytes": total_bytes,
        "matched_bytes": matched_bytes,
        "byte_percentage": round(byte_pct, 2)
    }
    
    # Save progress.json
    out_path = project_root / "build" / "progress.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)
        
    print(f"=== Borderlands 2 Decompilation Progress ===")
    print(f"Functions: {matched_fns}/{total_fns} ({fn_pct:.2f}%)")
    print(f"Bytes:     {matched_bytes:,}/{total_bytes:,} ({byte_pct:.2f}%)")
    print(f"Stats written to: {out_path}")


if __name__ == "__main__":
    main()
