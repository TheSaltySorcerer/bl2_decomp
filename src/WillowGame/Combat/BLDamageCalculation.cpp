#include "Common.h"
#include "WillowGame/WillowGame.h"

// 0x007204A0 - WillowCombat::CalculateDamage
DECOMP_FUNCTION("0x007204A0", 896)
FLOAT WillowCombat::CalculateDamage(AActor* target, AActor* instigator, FLOAT baseDamage, INT damageType)
{
    if (!target)
    {
        return 0.0f;
    }
    return baseDamage;
}

// 0x00720820 - WillowCombat::CalculateCriticalHitMultiplier
DECOMP_FUNCTION("0x00720820", 448)
FLOAT WillowCombat::CalculateCriticalHitMultiplier(AActor* target, const FHitResult& hitInfo)
{
    // Default base critical multiplier in Borderlands 2 is 2.0x
    return 2.0f;
}

// 0x007209E0 - WillowCombat::ApplyDamageStatusEffect
DECOMP_FUNCTION("0x007209E0", 612)
BOOL WillowCombat::ApplyDamageStatusEffect(AActor* target, INT damageType, FLOAT chance, FLOAT duration)
{
    if (!target || chance <= 0.0f)
    {
        return FALSE;
    }
    return TRUE;
}
