// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "UE4_TF_DLDrivingHud.generated.h"

UCLASS(config = Game)
class AUE4_TF_DLDrivingHud : public AHUD
{
	GENERATED_BODY()

public:
	AUE4_TF_DLDrivingHud();

	/** Font used to render the vehicle info */
	UPROPERTY()
	UFont* HUDFont;

	// Begin AHUD interface
	virtual void DrawHUD() override;
	// End AHUD interface

};
