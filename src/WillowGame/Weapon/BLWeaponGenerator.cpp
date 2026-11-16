#include "Common.h"
#include "WillowGame/WillowGame.h"

// 0x006B1240 - WillowWeaponPawn::GenerateWeaponParts
DECOMP_FUNCTION("0x006B1240", 768)
void WillowWeaponPawn::GenerateWeaponParts(int seed, FWeaponDefinition* def)
{
    this->WeaponSeed = seed;
    if (def)
    {
        this->Definition = *def;
    }
}

// 0x006B1540 - WillowWeaponPawn::CalculateStatModifiers
DECOMP_FUNCTION("0x006B1540", 1024)
void WillowWeaponPawn::CalculateStatModifiers(FWeaponStatModifiers* outModifiers)
{
    if (!outModifiers)
    {
        return;
    }

    outModifiers->DamageModifier = 1.0f;
    outModifiers->FireRateModifier = 1.0f;
    outModifiers->ReloadSpeedModifier = 1.0f;
    outModifiers->AccuracyModifier = 1.0f;
    outModifiers->RecoilModifier = 1.0f;
    outModifiers->MagazineCapacityModifier = 0;
}

// 0x006B1940 - WillowWeaponPawn::GetElementalDamageType
DECOMP_FUNCTION("0x006B1940", 256)
EElementalDamageType WillowWeaponPawn::GetElementalDamageType() const
{
    return this->ElementalType;
}
