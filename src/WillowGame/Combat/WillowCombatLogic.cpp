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


// 0x00611810 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611810", 27)
void __cdecl WillowCombatLogic::Sub_00611810(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168b970;
    }
}

// 0x00611830 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611830", 27)
void __cdecl WillowCombatLogic::Sub_00611830(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168baf8;
    }
}

// 0x00611850 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611850", 27)
void __cdecl WillowCombatLogic::Sub_00611850(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168bc80;
    }
}

// 0x00611870 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611870", 27)
void __cdecl WillowCombatLogic::Sub_00611870(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168be08;
    }
}

// 0x00611890 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611890", 27)
void __cdecl WillowCombatLogic::Sub_00611890(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168bf90;
    }
}


// 0x006118B0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x006118B0", 27)
void __cdecl WillowCombatLogic::Sub_006118B0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168c118;
    }
}

// 0x006118D0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x006118D0", 27)
void __cdecl WillowCombatLogic::Sub_006118D0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168c2a0;
    }
}

// 0x006118F0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x006118F0", 27)
void __cdecl WillowCombatLogic::Sub_006118F0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168c428;
    }
}

// 0x00611910 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611910", 27)
void __cdecl WillowCombatLogic::Sub_00611910(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168c5b0;
    }
}

// 0x00611930 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611930", 27)
void __cdecl WillowCombatLogic::Sub_00611930(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168c738;
    }
}

// 0x00611950 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611950", 27)
void __cdecl WillowCombatLogic::Sub_00611950(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168c8c0;
    }
}

// 0x00611970 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611970", 27)
void __cdecl WillowCombatLogic::Sub_00611970(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168ca48;
    }
}

// 0x00611990 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611990", 27)
void __cdecl WillowCombatLogic::Sub_00611990(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168cbd0;
    }
}

// 0x006119B0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x006119B0", 27)
void __cdecl WillowCombatLogic::Sub_006119B0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168cd58;
    }
}

// 0x006119D0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x006119D0", 27)
void __cdecl WillowCombatLogic::Sub_006119D0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168cee0;
    }
}

// 0x006119F0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x006119F0", 27)
void __cdecl WillowCombatLogic::Sub_006119F0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d068;
    }
}

// 0x00611A10 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611A10", 27)
void __cdecl WillowCombatLogic::Sub_00611A10(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d1f0;
    }
}

// 0x00611A30 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611A30", 27)
void __cdecl WillowCombatLogic::Sub_00611A30(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d378;
    }
}

// 0x00611A50 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611A50", 27)
void __cdecl WillowCombatLogic::Sub_00611A50(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d500;
    }
}

// 0x00611A70 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611A70", 27)
void __cdecl WillowCombatLogic::Sub_00611A70(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d688;
    }
}

// 0x00611A90 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611A90", 27)
void __cdecl WillowCombatLogic::Sub_00611A90(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d810;
    }
}

// 0x00611AB0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611AB0", 27)
void __cdecl WillowCombatLogic::Sub_00611AB0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168d998;
    }
}

// 0x00611AD0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611AD0", 27)
void __cdecl WillowCombatLogic::Sub_00611AD0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168db20;
    }
}

// 0x00611AF0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611AF0", 27)
void __cdecl WillowCombatLogic::Sub_00611AF0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168dca8;
    }
}

// 0x00611B10 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611B10", 27)
void __cdecl WillowCombatLogic::Sub_00611B10(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168de30;
    }
}

// 0x00611B30 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611B30", 27)
void __cdecl WillowCombatLogic::Sub_00611B30(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168dfb8;
    }
}

// 0x00611B50 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611B50", 27)
void __cdecl WillowCombatLogic::Sub_00611B50(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168e140;
    }
}

// 0x00611B70 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611B70", 27)
void __cdecl WillowCombatLogic::Sub_00611B70(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168e2c8;
    }
}

// 0x00611B90 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611B90", 27)
void __cdecl WillowCombatLogic::Sub_00611B90(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168e450;
    }
}

// 0x00611BB0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611BB0", 27)
void __cdecl WillowCombatLogic::Sub_00611BB0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168e5d8;
    }
}

// 0x00611BD0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611BD0", 27)
void __cdecl WillowCombatLogic::Sub_00611BD0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168e760;
    }
}

// 0x00611BF0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611BF0", 27)
void __cdecl WillowCombatLogic::Sub_00611BF0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168e8e8;
    }
}

// 0x00611C10 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611C10", 27)
void __cdecl WillowCombatLogic::Sub_00611C10(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168ea70;
    }
}

// 0x00611C30 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611C30", 27)
void __cdecl WillowCombatLogic::Sub_00611C30(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168ebf8;
    }
}

// 0x00611C50 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611C50", 27)
void __cdecl WillowCombatLogic::Sub_00611C50(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168ed80;
    }
}

// 0x00611C70 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611C70", 27)
void __cdecl WillowCombatLogic::Sub_00611C70(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168ef08;
    }
}

// 0x00611C90 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611C90", 27)
void __cdecl WillowCombatLogic::Sub_00611C90(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f090;
    }
}

// 0x00611CB0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611CB0", 27)
void __cdecl WillowCombatLogic::Sub_00611CB0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f218;
    }
}

// 0x00611CD0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611CD0", 27)
void __cdecl WillowCombatLogic::Sub_00611CD0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f3a0;
    }
}

// 0x00611CF0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611CF0", 27)
void __cdecl WillowCombatLogic::Sub_00611CF0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f528;
    }
}

// 0x00611D10 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611D10", 27)
void __cdecl WillowCombatLogic::Sub_00611D10(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f6b0;
    }
}

// 0x00611D30 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611D30", 27)
void __cdecl WillowCombatLogic::Sub_00611D30(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f838;
    }
}

// 0x00611D50 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611D50", 27)
void __cdecl WillowCombatLogic::Sub_00611D50(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168f9c0;
    }
}

// 0x00611D70 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611D70", 27)
void __cdecl WillowCombatLogic::Sub_00611D70(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168fb48;
    }
}

// 0x00611D90 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611D90", 27)
void __cdecl WillowCombatLogic::Sub_00611D90(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168fcd0;
    }
}

// 0x00611DB0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611DB0", 27)
void __cdecl WillowCombatLogic::Sub_00611DB0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168fe58;
    }
}

// 0x00611DD0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611DD0", 27)
void __cdecl WillowCombatLogic::Sub_00611DD0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x0168ffe0;
    }
}

// 0x00611DF0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611DF0", 27)
void __cdecl WillowCombatLogic::Sub_00611DF0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690168;
    }
}

// 0x00611E10 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611E10", 27)
void __cdecl WillowCombatLogic::Sub_00611E10(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x016902f0;
    }
}

// 0x00611E30 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611E30", 27)
void __cdecl WillowCombatLogic::Sub_00611E30(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690478;
    }
}

// 0x00611E50 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611E50", 27)
void __cdecl WillowCombatLogic::Sub_00611E50(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690600;
    }
}

// 0x00611E70 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611E70", 27)
void __cdecl WillowCombatLogic::Sub_00611E70(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690788;
    }
}

// 0x00611E90 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611E90", 27)
void __cdecl WillowCombatLogic::Sub_00611E90(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690910;
    }
}

// 0x00611EB0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611EB0", 27)
void __cdecl WillowCombatLogic::Sub_00611EB0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690a98;
    }
}

// 0x00611ED0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611ED0", 27)
void __cdecl WillowCombatLogic::Sub_00611ED0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690c20;
    }
}

// 0x00611EF0 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611EF0", 27)
void __cdecl WillowCombatLogic::Sub_00611EF0(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690da8;
    }
}

// 0x00611F10 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611F10", 27)
void __cdecl WillowCombatLogic::Sub_00611F10(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01690f30;
    }
}

// 0x00611F30 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611F30", 27)
void __cdecl WillowCombatLogic::Sub_00611F30(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x016910b8;
    }
}

// 0x00611F50 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611F50", 27)
void __cdecl WillowCombatLogic::Sub_00611F50(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x01691240;
    }
}

// 0x00611F70 - Archetype 2974536a049bafb3 Constructor Stub
DECOMP_FUNCTION("0x00611F70", 27)
void __cdecl WillowCombatLogic::Sub_00611F70(void* obj)
{
    if (obj)
    {
        reinterpret_cast<FBaseHelper_004ac0c0*>(obj)->Sub_004ac0c0();
        *reinterpret_cast<DWORD*>(obj) = 0x016913c8;
    }
}
