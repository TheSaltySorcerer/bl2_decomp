#pragma once

#ifndef BL2_DECOMP_COMMON_H
#define BL2_DECOMP_COMMON_H

#include <cstdint>
#include <cstddef>
#include <string>

// Windows types if compiling without windows.h
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

typedef int32_t   INT;
typedef uint32_t  UINT;
typedef int64_t   INT64;
typedef uint64_t  UINT64;
typedef float     FLOAT;
typedef double    DOUBLE;
typedef uint8_t   BYTE;
typedef uint16_t  WORD;
typedef uint32_t  DWORD;
typedef int32_t   BOOL;

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

// Unreal Engine 3 alignment and calling convention macros
#define FORCEINLINE __forceinline
#define VARARGS     __cdecl
#define CDECL       __cdecl
#define STDCALL     __stdcall

// Decompilation annotation macros matching fnv_decomp standards
#define MATCH_OFFSET(addr)
#define DECOMP_FUNCTION(addr, size)

#endif // BL2_DECOMP_COMMON_H
