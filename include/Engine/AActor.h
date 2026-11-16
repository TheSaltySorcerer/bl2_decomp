#pragma once

#ifndef BL2_DECOMP_AACTOR_H
#define BL2_DECOMP_AACTOR_H

#include "Core/UObject.h"

struct FHitResult
{
    FVector Location;
    FVector Normal;
    FLOAT   Time;
    void*   Actor;
    FName   BoneName;
    INT     Item;
    BYTE    PhysMaterial;
};

class AActor : public UObject
{
public:
    FVector Location;
    FRotator Rotation;
    FLOAT   DrawScale;
    FVector DrawScale3D;
    AActor* Owner;
    AActor* Base;
    BYTE    Physics;
    BYTE    Role;
    BYTE    RemoteRole;

    virtual void Tick(FLOAT DeltaTime) {}
    virtual void TakeDamage(FLOAT DamageAmount, void* DamageEvent, void* EventInstigator, AActor* DamageCauser) {}
};

#endif // BL2_DECOMP_AACTOR_H
