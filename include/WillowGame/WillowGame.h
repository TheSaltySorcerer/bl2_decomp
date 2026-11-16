#pragma once

#ifndef BL2_DECOMP_WILLOWGAME_H
#define BL2_DECOMP_WILLOWGAME_H

#include "Engine/AActor.h"

enum EElementalDamageType
{
    EDT_None       = 0,
    EDT_Incendiary = 1,
    EDT_Shock      = 2,
    EDT_Corrosive  = 3,
    EDT_Slag       = 4,
    EDT_Explosive  = 5
};

struct FWeaponDefinition
{
    FName BodyPart;
    FName GripPart;
    FName BarrelPart;
    FName SightPart;
    FName StockPart;
    FName ElementPart;
    FName AccessoryPart;
    FName MaterialPart;
};

struct FWeaponStatModifiers
{
    FLOAT DamageModifier;
    FLOAT FireRateModifier;
    FLOAT ReloadSpeedModifier;
    FLOAT AccuracyModifier;
    FLOAT RecoilModifier;
    INT   MagazineCapacityModifier;
};

class WillowWeaponPawn : public AActor
{
public:
    INT WeaponSeed;
    FWeaponDefinition Definition;
    FWeaponStatModifiers CachedModifiers;
    EElementalDamageType ElementalType;

    void GenerateWeaponParts(INT seed, FWeaponDefinition* def);
    void CalculateStatModifiers(FWeaponStatModifiers* outModifiers);
    EElementalDamageType GetElementalDamageType() const;
};

class WillowPlayerController : public AActor
{
public:
    FLOAT BleedoutRemaining;
    FLOAT BleedoutDuration;
    BOOL  bIsInFightForYourLife;
    INT   RespawnCost;

    void EnterFightForYourLife(FLOAT bleedoutTime);
    void TriggerSecondWind(AActor* killedEnemy);
    void RespawnAtNewUStation(void* station);
};

namespace WillowCombat
{
    FLOAT CalculateDamage(AActor* target, AActor* instigator, FLOAT baseDamage, INT damageType);
    FLOAT CalculateCriticalHitMultiplier(AActor* target, const FHitResult& hitInfo);
    BOOL  ApplyDamageStatusEffect(AActor* target, INT damageType, FLOAT chance, FLOAT duration);
}

#endif // BL2_DECOMP_WILLOWGAME_H
