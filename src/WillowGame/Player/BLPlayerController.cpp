#include "Common.h"
#include "WillowGame/WillowGame.h"

// 0x00843100 - WillowPlayerController::EnterFightForYourLife
DECOMP_FUNCTION("0x00843100", 412)
void WillowPlayerController::EnterFightForYourLife(float bleedoutTime)
{
    this->bIsInFightForYourLife = TRUE;
    this->BleedoutDuration = bleedoutTime;
    this->BleedoutRemaining = bleedoutTime;
}

// 0x008432A0 - WillowPlayerController::TriggerSecondWind
DECOMP_FUNCTION("0x008432A0", 288)
void WillowPlayerController::TriggerSecondWind(AActor* killedEnemy)
{
    this->bIsInFightForYourLife = FALSE;
    this->BleedoutRemaining = 0.0f;
}

// 0x008433C0 - WillowPlayerController::RespawnAtNewUStation
DECOMP_FUNCTION("0x008433C0", 576)
void WillowPlayerController::RespawnAtNewUStation(void* station)
{
    this->bIsInFightForYourLife = FALSE;
}
