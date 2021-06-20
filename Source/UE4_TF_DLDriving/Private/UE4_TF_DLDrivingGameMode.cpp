// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#include "UE4_TF_DLDrivingGameMode.h"
#include "UE4_TF_DLDrivingPawn.h"
#include "UE4_TF_DLDrivingHud.h"
#include "NN_ControlledPawn.h"

AUE4_TF_DLDrivingGameMode::AUE4_TF_DLDrivingGameMode()
{
	//DefaultPawnClass = ANN_ControlledPawn::StaticClass();
	HUDClass = AUE4_TF_DLDrivingHud::StaticClass();
}
