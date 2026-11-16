# Contributing to bl2_decomp

Thank you for your interest in contributing to **bl2_decomp**!

This project is a strict, 1:1 byte-matching decompilation of *Borderlands 2* (`Borderlands2.exe`, Steam v1.8.5). To maintain our strict legal clean-room standing and ensure binary accuracy, all contributions must adhere to the rules outlined below.

---

## ⚖️ Golden Rules of Clean-Room Decompilation

1. **NO Leaked Source Code:** You may NOT use, reference, or consult leaked proprietary source code from Gearbox Software, 2K Games, Epic Games, or any related parties.
2. **NO Copyrighted Assets:** Never commit game assets (textures, meshes, audio, dialogue files, `.upk` packages) to this repository. All assets remain strictly on the user's local disk via BYOG.
3. **NO Binary Blobs:** Never commit compiled executables (`.exe`), dynamic link libraries (`.dll`), or compiled object files (`.obj`).
4. **Byte-Accurate Matching Only:** Functions submitted as `matched: true` in `build/units.json` must compile to identical machine code bytes under the target MSVC toolset.

---

## 🛠️ Step-by-Step Function Decompilation Workflow

### Step 1: Claim a Function or Subsystem
1. Open `build/units.json` and select a function currently marked `"matched": false`.
2. Check open Pull Requests on GitHub to make sure another contributor is not already working on the same function.

### Step 2: Analyze the Target in Disassembly
1. Load your legal copy of `Borderlands2.exe` into **Ghidra** or **IDA Pro**.
2. Navigate to the function's virtual address (e.g. `0x006B1240`).
3. Identify:
   - Calling convention (`__thiscall`, `__cdecl`, `__stdcall`).
   - Function signature (parameters and return types).
   - Local variables and stack frame layout.
   - Loop structures, switch statements, and branch conditions.

### Step 3: Implement Clean C++
1. Locate the corresponding `.cpp` translation unit in `src/` (or create a new one if adding an unmapped unit).
2. Write the C++ implementation inside the file, wrapping it with the `DECOMP_FUNCTION(addr, size)` macro.
3. Use types and structures from `include/` (`UObject`, `AActor`, `FVector`, `FName`, etc.).

### Step 4: Verify with `build_and_match.py`
Run the local match checker against your executable:
```bash
python tools/build_and_match.py --image "<path_to_Borderlands2.exe>" --only <UnitName>
```

- If you see `[MATCH 100.0%]`: The compiled object bytes match the original binary byte-for-byte!
- If you see `[DIFF XX.X%]`: Use `python tools/diff.py <function_name>` to inspect instruction differences. Common issues include:
  - Register mismatches caused by variable declaration order.
  - Floating-point differences (ensure `/fp:fast` is used).
  - Loop unrolling or inlining differences.

### Step 5: Update Manifest & Submit PR
1. In `build/units.json`, set `"matched": true` for your verified function.
2. Run `python tools/check_progress.py` to regenerate `build/progress.json`.
3. Commit your changes with a clear message:
   ```bash
   git add src/ build/units.json build/progress.json
   git commit -m "WillowCombat: Match CalculateCriticalHitMultiplier (0x00720820)"
   ```
4. Push to your fork and submit a Pull Request. CI will automatically verify your byte match!
