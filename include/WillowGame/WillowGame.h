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
    INT Sub_00701300(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00701AF0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00701BB0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702030(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_007024C0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702550(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702610(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_007026B0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_007027E0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702C70(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702E20(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702F30(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00702FC0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703080(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703140(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_007031E0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703890(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703970(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703A00(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703B10(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703C50(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00703CD0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00704300(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00704470(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00704490(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_007044B0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00704540(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00704690(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_00704730(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
    INT Sub_007048E0(void* thisPtr, INT arg1 = 0, INT arg2 = 0);
}

#endif // BL2_DECOMP_WILLOWGAME_H
