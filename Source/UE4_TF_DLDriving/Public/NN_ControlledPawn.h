// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "UE4_TF_DLDrivingPawn.h"
#include "NN_ControlledPawn.generated.h"

/**
 * 
 */
UCLASS()
class UE4_TF_DLDRIVING_API ANN_ControlledPawn : public AUE4_TF_DLDrivingPawn
{
	GENERATED_BODY()

	UPROPERTY(Category = Component, VisibleDefaultsOnly, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	class UPythonComponent* PythonComp;

public:
	ANN_ControlledPawn();

	// Begin Pawn interface
	virtual void SetupPlayerInputComponent(UInputComponent* InputComponent) override;
	// End Pawn interface

	// Begin Actor interface
	virtual void Tick(float Delta) override;

	/** Max length of the raycast in front of the vehicle */
	UPROPERTY(Category = SensorsConfig, VisibleDefaultsOnly, BlueprintReadOnly)
	float MaxRaycastLengthFront;

	/** Max length of the raycast on the side of the vehicle */
	UPROPERTY(Category = SensorsConfig, VisibleDefaultsOnly, BlueprintReadOnly)
	float MaxRaycastLengthSide;

	/** Bounding Box of the vehicle */
	UPROPERTY(Category = SensorsConfig, VisibleDefaultsOnly, BlueprintReadOnly)
	FBox MainBBox;

	UPROPERTY(Category = SensorsConfig, EditAnywhere, BlueprintReadWrite)
	bool bEnablePlayerInput = true;

	UFUNCTION(BlueprintCallable)
	void ActuateActions(float forward, float right);

	UFUNCTION(BlueprintCallable)
	FString GetInputsString();
protected:
	virtual void BeginPlay() override;

};
