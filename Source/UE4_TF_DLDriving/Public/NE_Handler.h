// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "NE_Handler.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FStartFitnessComputation);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAgentFitnessComputed, int, index, float, fitness);

UCLASS()
class UE4_TF_DLDRIVING_API ANE_Handler : public AActor
{
	GENERATED_BODY()

	UPROPERTY(Category = Component, VisibleDefaultsOnly, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	class UPythonComponent* PythonComp;

public:	
	// Sets default values for this actor's properties
	ANE_Handler();

	UPROPERTY()
	FStartFitnessComputation OnStartFitnessComputation;

	UPROPERTY()
	FAgentFitnessComputed OnAgentFitnessComputed;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;
private:
	int NNNum;
	int BatchNum;
	int ProcessedAgents;

	UPROPERTY(EditDefaultsOnly, Category = Agent)
	TSubclassOf<AActor> NNAgent;

	UFUNCTION()
	void OnStartFitnessHandler();

	UFUNCTION()
	void AgentFitnessReturned(int index, float fitness);

	void InitializeAgentbatch();

	TArray<float> PopulationFitness;
};
