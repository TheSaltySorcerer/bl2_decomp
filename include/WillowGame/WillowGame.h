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

namespace WillowCombatLogic
{
    INT Sub_00701300(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00701AF0(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00701BB0(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00702030(void* thisPtr, INT arg1, INT arg2);
    INT Sub_007024C0(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00702550(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00702610(void* thisPtr, INT arg1, INT arg2);
    INT Sub_007026B0(void* thisPtr, INT arg1, INT arg2);
    INT Sub_007027E0(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00702C70(void* thisPtr, INT arg1, INT arg2);
    INT Sub_00702E20(void* thisPtr, INT arg1, INT arg2);
}

#endif // BL2_DECOMP_WILLOWGAME_H
