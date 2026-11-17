#!/usr/bin/env python3
"""
BL2_DECOMP: Sovereign Database Engine
Builds and maintains decomp_knowledge.db (SQLite WAL + FTS5):
Stores exact target binary code, SHA-256 byte hashes, structural opcode hashes,
class headers, disassembly, verified implementations, and high-water drafts.
Provides high-speed, lock-free, read-only search access for workers.
"""

import re
import json
import time
import hashlib
import sqlite3
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

PROJECT_ROOT = Path("M:/bl2_decomp")
TARGET_IMAGE = Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe")
DB_PATH = PROJECT_ROOT / "build" / "cache" / "decomp_knowledge.db"
MANIFEST_PATH = PROJECT_ROOT / "build" / "units.json"
HEADER_PATH = PROJECT_ROOT / "include" / "WillowGame" / "WillowGame.h"
COMBAT_CPP_PATH = PROJECT_ROOT / "src" / "WillowGame" / "Combat" / "WillowCombatLogic.cpp"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
pe = pefile.PE(str(TARGET_IMAGE), fast_load=True)
md = Cs(CS_ARCH_X86, CS_MODE_32)

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS functions (
        address TEXT PRIMARY KEY,
        name TEXT,
        unit TEXT,
        class_name TEXT,
        signature TEXT,
        header_declaration TEXT,
        size INTEGER,
        raw_bytes_hash TEXT,
        raw_bytes_hex TEXT,
        opcode_hash TEXT,
        disassembly TEXT,
        calling_convention TEXT,
        stack_args INTEGER,
        matched BOOLEAN DEFAULT 0,
        matched_code TEXT,
        high_water_code TEXT,
        high_water_pct REAL DEFAULT 0.0,
        iterations_stalled INTEGER DEFAULT 0,
        updated_at REAL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS archetypes (
        opcode_hash TEXT PRIMARY KEY,
        archetype_name TEXT,
        sample_addr TEXT,
        size INTEGER,
        template_code TEXT,
        member_count INTEGER DEFAULT 1,
        timestamp REAL
    );
    """)

    try:
        cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS functions_fts USING fts5(
            address UNINDEXED,
            name,
            class_name,
            header_declaration,
            disassembly,
            matched_code,
            high_water_code
        );
        """)
    except Exception:
        pass

    conn.commit()
    conn.close()

def compute_structural_opcode_hash(raw_bytes: bytes, va: int) -> tuple[str, str]:
    norm_tokens = []
    for inst in md.disasm(raw_bytes, va):
        norm_op = re.sub(r'0x[0-9a-fA-F]+', 'IMM', inst.op_str)
        norm_op = re.sub(r'\b[0-9]+\b', 'NUM', norm_op)
        norm_tokens.append(f"{inst.mnemonic}:{norm_op}")
    norm_str = ";".join(norm_tokens)
    return hashlib.sha256(norm_str.encode("utf-8")).hexdigest()[:16], norm_str

def populate_database():
    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    
    header_text = open(HEADER_PATH, encoding="utf-8").read() if HEADER_PATH.exists() else ""
    manifest = json.load(open(MANIFEST_PATH, encoding="utf-8"))
    
    # Parse existing matched code from WillowCombatLogic.cpp
    matched_implementations = {}
    if COMBAT_CPP_PATH.exists():
        cpp_text = open(COMBAT_CPP_PATH, encoding="utf-8").read()
        # Find functions: void WillowCombatLogic::Sub_xxxx(...) { ... }
        fn_blocks = re.findall(r"((?:void|INT|static void)\s+(?:__cdecl\s+|__stdcall\s+)?WillowCombatLogic::(Sub_[0-9A-Fa-f]{8})\s*\([^)]*\)\s*\{[^}]*\})", cpp_text)
        for full_fn, fn_name in fn_blocks:
            addr = "0x" + fn_name.split("_")[1].upper().zfill(8)
            matched_implementations[addr] = full_fn

    inserted = 0
    with open(TARGET_IMAGE, "rb") as f:
        for u in manifest.get("units", []):
            unit_name = u.get("name", "WillowGame")
            for fn in u.get("functions", []):
                addr = fn.get("address")
                fn_name = fn.get("name")
                size = fn.get("size", 32)
                va = int(addr, 16)
                
                # Extract raw machine code
                rva = va - pe.OPTIONAL_HEADER.ImageBase
                try:
                    offset = pe.get_offset_from_rva(rva)
                    f.seek(offset)
                    raw_bytes = f.read(size)
                except Exception:
                    continue

                raw_bytes_hash = hashlib.sha256(raw_bytes).hexdigest()
                raw_bytes_hex = raw_bytes.hex()
                opcode_h, norm_str = compute_structural_opcode_hash(raw_bytes, va)

                # Disassembly
                disasm_lines = []
                ret_bytes = 0
                uses_ecx = False
                disasm_objs = list(md.disasm(raw_bytes, va))
                for inst in disasm_objs:
                    disasm_lines.append(f"0x{inst.address:08X}: {inst.bytes.hex():12s} {inst.mnemonic:8s} {inst.op_str}")
                    if inst.mnemonic.startswith("ret") and inst.op_str.strip().isdigit():
                        ret_bytes = int(inst.op_str.strip())
                for inst in disasm_objs[:6]:
                    if "ecx" in inst.op_str and inst.mnemonic not in ("xor", "mov") and not inst.op_str.startswith("ecx,"):
                        uses_ecx = True
                        break

                call_conv = "__thiscall" if uses_ecx else ("__stdcall" if ret_bytes > 0 else "__cdecl")
                stack_args = ret_bytes // 4
                disassembly_str = "\n".join(disasm_lines)

                # Find header declaration
                fn_base = fn_name.split("::")[-1]
                m_header = re.search(r"([^\n;]*?" + re.escape(fn_base) + r"\s*\([^;]*\)\s*;)", header_text)
                header_decl = m_header.group(1).strip() if m_header else fn.get("signature", "")

                matched = fn.get("matched", False) or (addr in matched_implementations)
                matched_code = matched_implementations.get(addr, "")

                cur.execute("""
                INSERT OR REPLACE INTO functions (
                    address, name, unit, class_name, signature, header_declaration, size,
                    raw_bytes_hash, raw_bytes_hex, opcode_hash, disassembly,
                    calling_convention, stack_args, matched, matched_code,
                    high_water_code, high_water_pct, iterations_stalled, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    addr, fn_name, unit_name, "WillowCombatLogic", fn.get("signature", ""), header_decl, size,
                    raw_bytes_hash, raw_bytes_hex, opcode_h, disassembly_str,
                    call_conv, stack_args, 1 if matched else 0, matched_code,
                    "", 0.0, 0, time.time()
                ))

                try:
                    cur.execute("""
                    INSERT OR REPLACE INTO functions_fts (address, name, class_name, header_declaration, disassembly, matched_code, high_water_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """, (addr, fn_name, "WillowCombatLogic", header_decl, disassembly_str, matched_code, ""))
                except Exception:
                    pass

                inserted += 1

    # Populate Archetype table
    cur.execute("""
    SELECT opcode_hash, COUNT(*), MIN(address), AVG(size)
    FROM functions
    GROUP BY opcode_hash;
    """)
    archetype_rows = cur.fetchall()
    arch_inserted = 0
    for op_h, count, sample_addr, avg_sz in archetype_rows:
        # Check if any function in this archetype has a matched code
        cur.execute("SELECT matched_code FROM functions WHERE opcode_hash = ? AND matched = 1 LIMIT 1;", (op_h,))
        row = cur.fetchone()
        tmpl_code = row[0] if row and row[0] else ""
        cur.execute("""
        INSERT OR REPLACE INTO archetypes (opcode_hash, archetype_name, sample_addr, size, template_code, member_count, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (op_h, f"Archetype_{op_h}", sample_addr, int(avg_sz), tmpl_code, count, time.time()))
        arch_inserted += 1

    conn.commit()
    conn.close()
    print(f"\n[Sovereign Database Ready] Stored {inserted} functions in {DB_PATH.name}!")
    print(f"Discovered {arch_inserted} structural archetypes. Lock-free WAL mode active.")

if __name__ == "__main__":
    populate_database()
