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
    void Sub_00603960();
    void Sub_006059B0();
                static void __cdecl Sub_00603B90(void* a1);
                static void __cdecl Sub_00605B70(void* a1);
            static void __stdcall Sub_00607150(void* a1);
                static void __cdecl Sub_00611610(void* a1);
                static void __cdecl Sub_00611630(void* a1);
                static void __cdecl Sub_00611650(void* a1);
                static void __cdecl Sub_00611670(void* a1);
                static void __cdecl Sub_00611690(void* a1);
                static void __cdecl Sub_006116B0(void* a1);
                static void __cdecl Sub_006116D0(void* a1);
                static void __cdecl Sub_006116F0(void* a1);
                static void __cdecl Sub_00611710(void* a1);
                static void __cdecl Sub_00611730(void* a1);
                static void __cdecl Sub_00611750(void* a1);
                static void __cdecl Sub_00611770(void* a1);
                static void __cdecl Sub_00611790(void* a1);
                static void __cdecl Sub_006117B0(void* a1);
                static void __cdecl Sub_006117D0(void* a1);
                static void __cdecl Sub_006117F0(void* a1);
                static void __cdecl Sub_00611810(void* a1);
                static void __cdecl Sub_00611830(void* a1);
                static void __cdecl Sub_00611850(void* a1);
                static void __cdecl Sub_00611870(void* a1);
                static void __cdecl Sub_00611890(void* a1);
                static void __cdecl Sub_006118B0(void* a1);
                static void __cdecl Sub_006118D0(void* a1);
                static void __cdecl Sub_006118F0(void* a1);
                static void __cdecl Sub_00611910(void* a1);
                static void __cdecl Sub_00611930(void* a1);
                static void __cdecl Sub_00611950(void* a1);
                static void __cdecl Sub_00611970(void* a1);
                static void __cdecl Sub_00611990(void* a1);
                static void __cdecl Sub_006119B0(void* a1);
                static void __cdecl Sub_006119D0(void* a1);
                static void __cdecl Sub_006119F0(void* a1);
                static void __cdecl Sub_00611A10(void* a1);
                static void __cdecl Sub_00611A30(void* a1);
                static void __cdecl Sub_00611A50(void* a1);
                static void __cdecl Sub_00611A70(void* a1);
                static void __cdecl Sub_00611A90(void* a1);
                static void __cdecl Sub_00611AB0(void* a1);
                static void __cdecl Sub_00611AD0(void* a1);
                static void __cdecl Sub_00611AF0(void* a1);
                static void __cdecl Sub_00611B10(void* a1);
                static void __cdecl Sub_00611B30(void* a1);
                static void __cdecl Sub_00611B50(void* a1);
                static void __cdecl Sub_00611B70(void* a1);
                static void __cdecl Sub_00611B90(void* a1);
                static void __cdecl Sub_00611BB0(void* a1);
                static void __cdecl Sub_00611BD0(void* a1);
                static void __cdecl Sub_00611BF0(void* a1);
                static void __cdecl Sub_00611C10(void* a1);
                static void __cdecl Sub_00611C30(void* a1);
                static void __cdecl Sub_00611C50(void* a1);
                static void __cdecl Sub_00611C70(void* a1);
                static void __cdecl Sub_00611C90(void* a1);
                static void __cdecl Sub_00611CB0(void* a1);
                static void __cdecl Sub_00611CD0(void* a1);
                static void __cdecl Sub_00611CF0(void* a1);
                static void __cdecl Sub_00611D10(void* a1);
                static void __cdecl Sub_00611D30(void* a1);
                static void __cdecl Sub_00611D50(void* a1);
                static void __cdecl Sub_00611D70(void* a1);
                static void __cdecl Sub_00611D90(void* a1);
                static void __cdecl Sub_00611DB0(void* a1);
                static void __cdecl Sub_00611DD0(void* a1);
                static void __cdecl Sub_00611DF0(void* a1);
                static void __cdecl Sub_00611E10(void* a1);
                static void __cdecl Sub_00611E30(void* a1);
                static void __cdecl Sub_00611E50(void* a1);
                static void __cdecl Sub_00611E70(void* a1);
                static void __cdecl Sub_00611E90(void* a1);
                static void __cdecl Sub_00611EB0(void* a1);
                static void __cdecl Sub_00611ED0(void* a1);
                static void __cdecl Sub_00611EF0(void* a1);
                static void __cdecl Sub_00611F10(void* a1);
                static void __cdecl Sub_00611F30(void* a1);
                static void __cdecl Sub_00611F50(void* a1);
                static void __cdecl Sub_00611F70(void* a1);
                static void __stdcall Sub_00701300(void* a1, void* a2);
                static void __cdecl Sub_00701AF0(void* a1);
                static void __stdcall Sub_00701BB0(void* a1);
        static void __stdcall Sub_00702030(void* a1, void* a2);
                static void __stdcall Sub_007024C0(void* a1, void* a2);
                static void __stdcall Sub_00702550(void* a1);
            static void __stdcall Sub_00702610(void* a1, void* a2);
                static void __stdcall Sub_007026B0(void* a1, void* a2);
                static void __stdcall Sub_007027E0(void* a1);
                static void __stdcall Sub_00702C70(void* a1, void* a2);
                static void __cdecl Sub_00702E20(void* a1, void* a2, void* a3);
            static void __stdcall Sub_00702F30(void* a1, void* a2);
            static void __stdcall Sub_00702FC0(void* a1, void* a2);
                static void __cdecl Sub_00703080(void* a1, void* a2, void* a3);
                static void __stdcall Sub_00703140(void* a1);
                static void __stdcall Sub_007031E0(void* a1);
                static void __stdcall Sub_00703890(void* a1);
                static void __stdcall Sub_00703970(void* a1);
                static void __stdcall Sub_00703A00(void* a1);
                static void __cdecl Sub_00703B10(void* a1, void* a2, void* a3, void* a4, void* a5, void* a6, void* a7);
                static void __cdecl Sub_00703C50(void* a1, void* a2, void* a3, void* a4, void* a5, void* a6, void* a7);
            void Sub_00703CD0();
                static void __stdcall Sub_00704300(void* a1);
            static void __stdcall Sub_00704470(void* a1, void* a2, void* a3);
            static void __stdcall Sub_00704490(void* a1, void* a2, void* a3);
                static void __cdecl Sub_007044B0(void* a1, void* a2, void* a3);
            void Sub_00704540(void* a1);
                static void __stdcall Sub_00704690(void* a1);
                static void __stdcall Sub_00704730(void* a1, void* a2);
                static void __cdecl Sub_007048E0(void* a1, void* a2, void* a3, void* a4, void* a5, void* a6);
};

#endif // BL2_DECOMP_WILLOWGAME_H