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

class WillowCombatLogic
{
public:
    BYTE pad_0x00[0x50];
    INT Field_0x50;

        static void __stdcall Sub_006097B0(void* a1);
            static void __cdecl Sub_00603B90();
            static void __cdecl Sub_00605B70();
            static void __stdcall Sub_00607150(void* a1);
            static void __cdecl Sub_00611610();
            static void __cdecl Sub_00611630();
            static void __cdecl Sub_00611650();
            static void __cdecl Sub_00611670();
            static void __cdecl Sub_00611690();
            static void __cdecl Sub_006116B0();
            static void __cdecl Sub_006116D0();
            static void __cdecl Sub_006116F0();
            static void __cdecl Sub_00611710();
            static void __cdecl Sub_00611730();
            static void __cdecl Sub_00611750();
            static void __cdecl Sub_00611770();
            static void __cdecl Sub_00611790();
            static void __cdecl Sub_006117B0();
            static void __cdecl Sub_006117D0();
            static void __cdecl Sub_006117F0();
            static void __cdecl Sub_00611810();
            static void __cdecl Sub_00611830();
            static void __cdecl Sub_00611850();
            static void __cdecl Sub_00611870();
            static void __cdecl Sub_00611890();
            static void __cdecl Sub_006118B0();
            static void __cdecl Sub_006118D0();
            static void __cdecl Sub_006118F0();
            static void __cdecl Sub_00611910();
            static void __cdecl Sub_00611930();
            static void __cdecl Sub_00611950();
            static void __cdecl Sub_00611970();
            static void __cdecl Sub_00611990();
            static void __cdecl Sub_006119B0();
            static void __cdecl Sub_006119D0();
            static void __cdecl Sub_006119F0();
            static void __cdecl Sub_00611A10();
            static void __cdecl Sub_00611A30();
            static void __cdecl Sub_00611A50();
            static void __cdecl Sub_00611A70();
            static void __cdecl Sub_00611A90();
            static void __cdecl Sub_00611AB0();
            static void __cdecl Sub_00611AD0();
            static void __cdecl Sub_00611AF0();
            static void __cdecl Sub_00611B10();
            static void __cdecl Sub_00611B30();
            static void __cdecl Sub_00611B50();
            static void __cdecl Sub_00611B70();
            static void __cdecl Sub_00611B90();
            static void __cdecl Sub_00611BB0();
            static void __cdecl Sub_00611BD0();
            static void __cdecl Sub_00611BF0();
            static void __cdecl Sub_00611C10();
            static void __cdecl Sub_00611C30();
            static void __cdecl Sub_00611C50();
            static void __cdecl Sub_00611C70();
            static void __cdecl Sub_00611C90();
            static void __cdecl Sub_00611CB0();
            static void __cdecl Sub_00611CD0();
            static void __cdecl Sub_00611CF0();
            static void __cdecl Sub_00611D10();
            static void __cdecl Sub_00611D30();
            static void __cdecl Sub_00611D50();
            static void __cdecl Sub_00611D70();
            static void __cdecl Sub_00611D90();
            static void __cdecl Sub_00611DB0();
            static void __cdecl Sub_00611DD0();
            static void __cdecl Sub_00611DF0();
            static void __cdecl Sub_00611E10();
            static void __cdecl Sub_00611E30();
            static void __cdecl Sub_00611E50();
            static void __cdecl Sub_00611E70();
            static void __cdecl Sub_00611E90();
            static void __cdecl Sub_00611EB0();
            static void __cdecl Sub_00611ED0();
            static void __cdecl Sub_00611EF0();
            static void __cdecl Sub_00611F10();
            static void __cdecl Sub_00611F30();
            static void __cdecl Sub_00611F50();
            static void __cdecl Sub_00611F70();
            static void __cdecl Sub_00701300();
            static void __cdecl Sub_00701AF0();
            static void __cdecl Sub_00701BB0();
        static void __stdcall Sub_00702030(void* a1, void* a2);
            static void __cdecl Sub_007024C0();
            static void __cdecl Sub_00702550();
            static void __stdcall Sub_00702610(void* a1, void* a2);
            static void __cdecl Sub_007026B0();
            static void __cdecl Sub_007027E0();
            static void __cdecl Sub_00702C70();
            static void __cdecl Sub_00702E20();
            static void __stdcall Sub_00702F30(void* a1, void* a2);
            static void __stdcall Sub_00702FC0(void* a1, void* a2);
            static void __cdecl Sub_00703080();
            static void __cdecl Sub_00703140();
            static void __cdecl Sub_007031E0();
            static void __cdecl Sub_00703890();
            static void __cdecl Sub_00703970();
            static void __cdecl Sub_00703A00();
            static void __cdecl Sub_00703B10();
            static void __cdecl Sub_00703C50();
            void Sub_00703CD0();
            static void __cdecl Sub_00704300();
            static void __cdecl Sub_00704470();
            static void __cdecl Sub_00704490();
            static void __cdecl Sub_007044B0();
            void Sub_00704540(void* a1);
            static void __cdecl Sub_00704690();
            static void __cdecl Sub_00704730();
            static void __cdecl Sub_007048E0();
};

#endif // BL2_DECOMP_WILLOWGAME_H