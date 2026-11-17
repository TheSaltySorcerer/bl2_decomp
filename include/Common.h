#pragma once

#ifndef BL2_DECOMP_COMMON_H
#define BL2_DECOMP_COMMON_H

#include <cstdint>
#include <cstddef>
#include <string>

#ifdef _WIN32
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#else
typedef int32_t   INT;
typedef uint32_t  UINT;
typedef uint8_t   BYTE;
typedef uint16_t  WORD;
typedef uint32_t  DWORD;
typedef int32_t   BOOL;
#endif

typedef int64_t   INT64;
typedef uint64_t  UINT64;
typedef float     FLOAT;
typedef double    DOUBLE;

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

// Unreal Engine 3 alignment and calling convention macros
#define FORCEINLINE __forceinline
#define VARARGS     __cdecl
#ifndef CDECL
#define CDECL       __cdecl
#endif
#ifndef STDCALL
#define STDCALL     __stdcall
#endif

// Decompilation annotation macros matching fnv_decomp standards
#define MATCH_OFFSET(addr)
#define DECOMP_FUNCTION(addr, size)

// Global BL2 engine stubs
void Init_004050f0();
struct FBL2GlobalDispatcher {
    void** vtbl;
    void Init_004050f0() { ::Init_004050f0(); }
};
extern FBL2GlobalDispatcher* g_GlobalObj_19f29a4;

#endif // BL2_DECOMP_COMMON_H

void __stdcall Sub_006fb980(void* a1, void* a2);

struct FBaseHelper_004ac0c0 { void Sub_004ac0c0(); };
