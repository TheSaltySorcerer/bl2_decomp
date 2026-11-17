import sqlite3
import json
import re
import hashlib
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

PROJECT_ROOT = Path("M:/bl2_decomp")
TARGET_IMAGE = Path(r"M:\BL2-64bit-lab\BL2-reference\Binaries\Win32\Borderlands2.exe")
DB_PATH = PROJECT_ROOT / "build" / "cache" / "decomp_cache.db"
MANIFEST_PATH = PROJECT_ROOT / "build" / "units.json"

pe = pefile.PE(str(TARGET_IMAGE), fast_load=True)
md = Cs(CS_ARCH_X86, CS_MODE_32)

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("PRAGMA synchronous=NORMAL;")

# Create base tables
cur.execute("""
CREATE TABLE IF NOT EXISTS high_water_drafts (
    address TEXT PRIMARY KEY,
    unit TEXT,
    size INTEGER,
    match_pct REAL,
    code TEXT,
    worker_id TEXT,
    iterations_stalled INTEGER DEFAULT 0,
    timestamp REAL,
    opcode_hash TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS archetypes (
    opcode_hash TEXT PRIMARY KEY,
    archetype_name TEXT,
    sample_addr TEXT,
    size INTEGER,
    template_code TEXT,
    timestamp REAL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS function_archetype_links (
    address TEXT PRIMARY KEY,
    opcode_hash TEXT,
    norm_opcodes TEXT,
    size INTEGER
);
""")

# FTS5 tables
try:
    cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS high_water_fts USING fts5(address UNINDEXED, unit, code);")
    cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS archetypes_fts USING fts5(opcode_hash UNINDEXED, archetype_name, template_code);")
except Exception:
    pass

def compute_structural_opcode_hash(va: int, size: int) -> tuple[str, str]:
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    offset = pe.get_offset_from_rva(rva)
    with open(TARGET_IMAGE, "rb") as f:
        f.seek(offset)
        raw_bytes = f.read(size)
    norm_tokens = []
    for inst in md.disasm(raw_bytes, va):
        norm_op = re.sub(r'0x[0-9a-fA-F]+', 'IMM', inst.op_str)
        norm_op = re.sub(r'\b[0-9]+\b', 'NUM', norm_op)
        norm_tokens.append(f"{inst.mnemonic}:{norm_op}")
    norm_str = ";".join(norm_tokens)
    h = hashlib.sha256(norm_str.encode("utf-8")).hexdigest()[:16]
    return h, norm_str

# Index all functions from units.json
manifest = json.load(open(MANIFEST_PATH))
linked = 0
for u in manifest.get("units", []):
    for fn in u.get("functions", []):
        addr = fn.get("address")
        va = int(addr, 16)
        sz = fn.get("size", 32)
        try:
            h, norm_str = compute_structural_opcode_hash(va, sz)
            cur.execute("""
            INSERT OR REPLACE INTO function_archetype_links (address, opcode_hash, norm_opcodes, size)
            VALUES (?, ?, ?, ?);
            """, (addr, h, norm_str, sz))
            linked += 1
        except Exception:
            pass

# Pre-populate archetypes from archetypes.json
arch_file = PROJECT_ROOT / "build" / "cache" / "archetypes.json"
arch_count = 0
if arch_file.exists():
    arch_data = json.load(open(arch_file))
    for h, d in arch_data.items():
        cur.execute("""
        INSERT OR REPLACE INTO archetypes (opcode_hash, archetype_name, sample_addr, size, template_code, timestamp)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (h, d.get("archetype_name", "Archetype"), d.get("sample_addr", ""), d.get("size", 0), d.get("template_code", ""), 0.0))
        try:
            cur.execute("INSERT OR REPLACE INTO archetypes_fts (opcode_hash, archetype_name, template_code) VALUES (?, ?, ?);",
                        (h, d.get("archetype_name", "Archetype"), d.get("template_code", "")))
        except Exception:
            pass
        arch_count += 1

conn.commit()
conn.close()

print(f"Migration complete: Linked {linked} functions to opcode hashes in SQLite WAL database.")
print(f"Loaded {arch_count} verified archetypes into archetypes table and FTS5 search index.")
