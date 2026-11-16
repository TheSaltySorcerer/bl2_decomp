#include "Common.h"
#include "WillowGame/WillowGame.h"

// ============================================================================
// WillowCombatLogic Implementation
// Clean-Room 1:1 Byte-Matching Decompilation for Borderlands 2 (Win32 v1.8.5)
// Target Binary SHA-256: 1231b384aea791bc51286664627d03e27d6a77ffd4ec3bb5001186c136504c17
// ============================================================================

// Address: 0x006097B0 (13 bytes)
// Emitted: 55 8b ec 8b 45 08 89 41 50 5d c2 04 00
// Target:  55 8b ec 8b 45 08 89 41 50 5d c2 04 00
// Verified: 100.0% Exact Byte Match (MSVC /O2 /Oi /Ot /Oy- /GF /EHsc /MT /fp:fast)
void WillowCombatLogic::Sub_006097B0(INT val)
{
    Field_0x50 = val;
}
