# bl2_decomp

[![CI Match Check](https://github.com/TheSaltySorcerer/bl2_decomp/actions/workflows/match.yml/badge.svg)](https://github.com/TheSaltySorcerer/bl2_decomp/actions/workflows/match.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20x86%20%7C%20x64-green.svg)](#)
[![Methodology](https://img.shields.io/badge/Methodology-fnv__decomp%20Byte--Exact-orange.svg)](#methodology)

An open-source, community-driven, **1:1 byte-accurate C++ source code decompilation** of **Borderlands 2** (PC Steam v1.8.5, `Borderlands2.exe`).

Inspired directly by the architecture and methodology of [**`momusdigital/fnv_decomp`**](https://github.com/momusdigital/fnv_decomp) (*Fallout: New Vegas*) and **`f3decomp`** (*Fallout 3*).

---

## 🎯 Project Goals

1. **Byte-for-Byte Source Parity:** Reverse-engineer all functions within `Borderlands2.exe` into clean, human-readable C++ that compiles down to the exact identical machine code bytes of the original retail executable.
2. **Game Preservation & Historical Reference:** Create an authoritative, fully documented reference of Gearbox Software's **WillowEngine** (a customized Unreal Engine 3 fork), preserving procedural weapon generation, combat scaling, AI behavior trees, and the New-U state machine for future generations.
3. **Foundation for Native 64-Bit Recompilation:** A complete 1:1 C++ decompilation serves as the launchpad for modern native 64-bit engine ports (`OpenWillow`), native Linux/Steam Deck execution, unconstrained physics framerates, and true multiplayer/co-op overhauls.

---

## ⚖️ Legal & Clean-Room Statement

> [!IMPORTANT]
> **Strict "Bring Your Own Game" (BYOG) Policy**
>
> This repository contains **NO game assets, NO copyrighted 3D models, NO textures, NO audio files, NO level scripts, and NO proprietary Gearbox/2K binary executables.**
>
> To compile, verify, or interact with this codebase, you must legally own a licensed copy of **Borderlands 2** on Steam. All tests and comparisons require pointing the build tools to your local, legally purchased `Borderlands2.exe`.
>
> This project is for educational, research, and software preservation purposes under Fair Use. It is not affiliated with, sponsored by, or endorsed by Gearbox Software, 2K Games, or Take-Two Interactive.

---

## 🔬 Methodology: The Automated Match Pipeline

This project operates on the same strict byte-matching verification pipeline popularized by **Momus Digital** for *Fallout: New Vegas*:

```
+-------------------------------------------------------------------------+
|                    bl2_decomp Verification Pipeline                     |
+-------------------------------------------------------------------------+
                                     |
                                     v
                 [ User Supplies Legal Borderlands2.exe ]
                                     |
                                     +--------------------+
                                     |                    |
                                     v                    v
                          [ SHA-256 Validation ]   [ Extract Target Bytes ]
                                     |                    |
   [ C++ Source (src/) ]             |                    |
            |                        |                    |
            v                        |                    |
   [ Compile via MSVC ]              |                    |
            |                        |                    |
            v                        |                    |
   [ Extract .obj Opcodes ]          |                    |
            |                        |                    |
            +------------------------+--------------------+
                                     |
                                     v
                        [ tools/build_and_match.py ]
                                     |
            +------------------------+------------------------+
            |                                                 |
            v                                                 v
   [ 100% Byte-for-Byte Match ]                     [ Assembly Mismatch ]
            |                                                 |
   Commit & Update Progress                          Display Opcode Diff
```

### 1. Translation Units (`build/units.json`)
The entire binary is partitioned into discrete translation units matching WillowEngine subsystems (`WillowGame`, `Engine`, `Core`, `GearboxFramework`). Every function is cataloged by its virtual address, byte size, signature, and match status.

### 2. Automated Matching (`tools/build_and_match.py`)
Contributors compile translation units using Microsoft Visual C++ (`MSVC`). The tool extracts generated object code, relocates addresses, and validates byte-accuracy against the original binary at the mapped address.

### 3. CI/CD Parity Gating (`.github/workflows/match.yml`)
Every pull request is automatically tested against the binary in CI. If a proposed change introduces an instruction mismatch or breaks binary parity, the PR cannot be merged.

---

## 🛠️ Getting Started

### Prerequisites
- **OS:** Windows 10/11 or Linux with Wine
- **Python:** Python 3.10+
- **Compiler:** Microsoft Visual C++ (Visual Studio 2010 SP1 / MSVC v100 toolset, or modern MSVC with `/O2 /fp:fast` flags)
- **Game Executable:** Legally owned Steam release of `Borderlands2.exe` (v1.8.5)
  - Target SHA-256: `1231b384aea791bc51286664627d03e27d6a77ffd4ec3bb5001186c136504c17`

### Setup & Verification

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TheSaltySorcerer/bl2_decomp.git
   cd bl2_decomp
   ```

2. **Verify manifest syntax (Dry Run):**
   ```bash
   python tools/build_and_match.py --dry-run
   ```

3. **Run the match pipeline against your local binary:**
   ```bash
   python tools/build_and_match.py --image "C:\Program Files (x86)\Steam\steamapps\common\Borderlands 2\Binaries\Win32\Borderlands2.exe"
   ```

4. **Test a single unit:**
   ```bash
   python tools/build_and_match.py --image "<path_to_Borderlands2.exe>" --only BLWeaponGenerator
   ```

5. **Generate progress report:**
   ```bash
   python tools/check_progress.py
   ```

---

## 📁 Repository Structure

```
bl2_decomp/
├── .github/
│   └── workflows/
│       └── match.yml          # Automated CI/CD byte-matching runner
├── build/
│   ├── units.json             # Function registry, address map, and compiler options
│   └── progress.json          # Live decompilation progress metrics
├── include/
│   ├── Common.h               # Fundamental types and decomp macros
│   ├── Core/
│   │   └── UObject.h          # Unreal Engine 3 base object reflection
│   ├── Engine/
│   │   └── AActor.h           # World actor primitives and hit results
│   ├── GearboxFramework/     # Gearbox specialized subsystem headers
│   └── WillowGame/
│       └── WillowGame.h       # Borderlands 2 specific game structures
├── src/
│   ├── main.cpp               # WinMain & WillowEngine entry point
│   └── WillowGame/
│       ├── Combat/
│       │   └── BLDamageCalculation.cpp  # Damage, elemental status, and criticals
│       ├── Player/
│       │   └── BLPlayerController.cpp   # FFYL, Second Wind, and New-U loop
│       └── Weapon/
│           └── BLWeaponGenerator.cpp    # Procedural part assembly & stat scaling
├── tools/
│   ├── build_and_match.py     # Core compiler & byte-comparison engine
│   ├── check_progress.py      # Statistical progress counter
│   └── diff.py                # Instruction-level disassembly comparison
├── CONTRIBUTING.md            # Clean-room decompilation contribution guide
├── LICENSE                    # GNU General Public License v3.0
└── README.md                  # This file
```

---

## 🤝 Contributing

We welcome contributions from reverse engineers, systems programmers, and AI tooling researchers!

Before submitting code, please review [**`CONTRIBUTING.md`**](CONTRIBUTING.md) to understand:
- The clean-room decompilation protocol.
- How to extract functions from Ghidra / IDA Pro.
- Matching compiler optimization flags and register allocation.
- Updating `build/units.json`.

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. See [LICENSE](LICENSE) for details.

*Borderlands, Borderlands 2, Gearbox Software, and 2K Games are trademarks or registered trademarks of Gearbox Software, LLC and Take-Two Interactive Software, Inc. This project is not affiliated with or endorsed by Gearbox or 2K.*
