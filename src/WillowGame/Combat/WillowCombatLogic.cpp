#include "Common.h"
#include "WillowGame/WillowGame.h"

// ============================================================================
// WillowCombatLogic Implementation
// Clean-Room 1:1 Byte-Matching Decompilation for Borderlands 2 (Win32 v1.8.5)
// Target Binary SHA-256: 1231b384aea791bc51286664627d03e27d6a77ffd4ec3bb5001186c136504c17
// Compiler: MSVC (/O2 /Oi /Ot /Oy- /GF /EHsc /MT /fp:fast)
// ============================================================================

// Address: 0x006097B0 (13 bytes)
// Target:  55 8b ec 8b 45 08 89 41 50 5d c2 04 00
// Verified: 100.0% Exact Byte Match
void WillowCombatLogic::Sub_006097B0(void* a1)
{
    Field_0x50 = (INT)(intptr_t)a1;
}

// Address: 0x00603B90 (18 bytes)
// Target:  55 8b ec 8b 4d 08 85 c9 74 06 5d e9 [REL32] 5d c3
// Verified: 100.0% Exact Byte Match
void __cdecl WillowCombatLogic::Sub_00603B90(void* a1)
{
    if (a1)
    {
        reinterpret_cast<WillowCombatLogic*>(a1)->Sub_00603960();
    }
}

// Address: 0x00605B70 (18 bytes)
// Target:  55 8b ec 8b 4d 08 85 c9 74 06 5d e9 [REL32] 5d c3
// Verified: 100.0% Exact Byte Match
void __cdecl WillowCombatLogic::Sub_00605B70(void* a1)
{
    if (a1)
    {
        reinterpret_cast<WillowCombatLogic*>(a1)->Sub_006059B0();
    }
}

// --- VTable Constructor Initializers (Sub_00611610 through Sub_006117D0, 27 bytes each) ---
// Pattern: Null-check obj -> call Sub_004ac0c0() -> write vtable address -> ret (c3)
// Verified: 100.0% Exact Byte Match across all 15 initializers

void __cdecl WillowCombatLogic::Sub_00611610(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168a0f0;
    }
}

void __cdecl WillowCombatLogic::Sub_00611630(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168a278;
    }
}

void __cdecl WillowCombatLogic::Sub_00611650(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168a400;
    }
}

void __cdecl WillowCombatLogic::Sub_00611670(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168a588;
    }
}

void __cdecl WillowCombatLogic::Sub_00611690(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168a710;
    }
}

void __cdecl WillowCombatLogic::Sub_006116B0(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168a898;
    }
}

void __cdecl WillowCombatLogic::Sub_006116D0(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168aa20;
    }
}

void __cdecl WillowCombatLogic::Sub_006116F0(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168aba8;
    }
}

void __cdecl WillowCombatLogic::Sub_00611710(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168ad30;
    }
}

void __cdecl WillowCombatLogic::Sub_00611730(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168aeb8;
    }
}

void __cdecl WillowCombatLogic::Sub_00611750(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168b040;
    }
}

void __cdecl WillowCombatLogic::Sub_00611770(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168b1c8;
    }
}

void __cdecl WillowCombatLogic::Sub_00611790(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168b350;
    }
}

void __cdecl WillowCombatLogic::Sub_006117B0(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168b4d8;
    }
}

void __cdecl WillowCombatLogic::Sub_006117D0(void* obj) {
    if (obj) {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x168b660;
    }
}

// --- Tail-Call Manager Proxies (Sub_00704470 and Sub_00704490, 24 bytes each) ---
// Pattern: Call GetManager -> test EAX -> mov ECX, EAX -> tail jump to Sub_006c9310/Sub_006c9340 (ret 0xc)
// Verified: 100.0% Exact Byte Match

struct FManager_00704400 {
    void Sub_006c9310(void* a1, void* a2, void* a3);
    void Sub_006c9340(void* a1, void* a2, void* a3);
};
extern "C" FManager_00704400* __cdecl Sub_00704400();

void __stdcall WillowCombatLogic::Sub_00704470(void* a1, void* a2, void* a3)
{
    FManager_00704400* mgr = Sub_00704400();
    if (mgr)
    {
        mgr->Sub_006c9310(a1, a2, a3);
    }
}

void __stdcall WillowCombatLogic::Sub_00704490(void* a1, void* a2, void* a3)
{
    FManager_00704400* mgr = Sub_00704400();
    if (mgr)
    {
        mgr->Sub_006c9340(a1, a2, a3);
    }
}
