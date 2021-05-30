// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#include "UE4_TF_DLDrivingGameMode.h"
#include "UE4_TF_DLDrivingPawn.h"
#include "UE4_TF_DLDrivingHud.h"

AUE4_TF_DLDrivingGameMode::AUE4_TF_DLDrivingGameMode()
{
	DefaultPawnClass = AUE4_TF_DLDrivingPawn::StaticClass();
	HUDClass = AUE4_TF_DLDrivingHud::StaticClass();
}
