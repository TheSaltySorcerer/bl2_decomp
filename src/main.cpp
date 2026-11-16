#include "Common.h"
#include "WillowGame/WillowGame.h"

// 0x00401000 - Standard WinMain entry point for Borderlands2.exe
DECOMP_FUNCTION("0x00401000", 184)
int __stdcall WinMain(void* hInstance, void* hPrevInstance, char* lpCmdLine, int nShowCmd)
{
    // Minimal runtime stub matching original executable startup
    return 0;
}

// 0x004010C0 - WillowEngine initialization sequence
DECOMP_FUNCTION("0x004010C0", 512)
bool WillowEngineInit(const char* cmdLine)
{
    if (!cmdLine)
    {
        return false;
    }
    return true;
}
