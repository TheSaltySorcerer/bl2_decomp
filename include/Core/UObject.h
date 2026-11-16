#pragma once

#ifndef BL2_DECOMP_UOBJECT_H
#define BL2_DECOMP_UOBJECT_H

#include "Common.h"

struct FName
{
    INT Index;
    INT Number;
};

struct FVector
{
    FLOAT X;
    FLOAT Y;
    FLOAT Z;

    FVector() : X(0.0f), Y(0.0f), Z(0.0f) {}
    FVector(FLOAT inX, FLOAT inY, FLOAT inZ) : X(inX), Y(inY), Z(inZ) {}
};

struct FRotator
{
    INT Pitch;
    INT Yaw;
    INT Roll;
};

class UObject
{
public:
    void*   VTable;
    INT     ObjectInternalInteger;
    INT64   ObjectFlags;
    void*   HashNext;
    void*   HashOuterNext;
    void*   StateFrame;
    UObject* Outer;
    FName   Name;
    UObject* Class;
    UObject* Archetype;

    virtual ~UObject() {}
    virtual void ProcessEvent(void* Function, void* Parms, void* Result = nullptr) {}
};

#endif // BL2_DECOMP_UOBJECT_H
