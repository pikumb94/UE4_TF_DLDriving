// Fill out your copyright notice in the Description page of Project Settings.


#include "NE_Handler.h"
#include "Engine/Engine.h"
#include "PythonComponent.h"
#include "NN_ControlledPawn.h"

// Sets default values
ANE_Handler::ANE_Handler()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	PythonComp = CreateDefaultSubobject<UPythonComponent>(TEXT("PyComponent"));
	PythonComp->PythonModule = PythonComp->PythonClass = "NEHandler";

	NNAgent = ANN_ControlledPawn::StaticClass();

	OnStartFitnessComputation.AddDynamic(this, &ANE_Handler::OnStartFitnessHandler);
	OnAgentFitnessComputed.AddDynamic(this, &ANE_Handler::AgentFitnessReturned);
	BatchNum = 5;

}

// Called when the game starts or when spawned
void ANE_Handler::BeginPlay()
{
	Super::BeginPlay();
}

// Called every frame
void ANE_Handler::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

void ANE_Handler::OnStartFitnessHandler()
{

	NNNum = PythonComp->CallPythonComponentMethodInt(FString("get_PopulationSize"), FString());
	PopulationFitness.Init(-1, NNNum);
	ProcessedAgents = 0;

	InitializeAgentbatch();

}

void ANE_Handler::AgentFitnessReturned(int index, float fitness)
{
	if (GEngine) {

		GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("MORTO! %d"), NNNum));

	}

	PopulationFitness[index] = fitness;

	ProcessedAgents++;

	if(ProcessedAgents >= NNNum)
	{
		FString StringifiedArray;
		for (auto e : PopulationFitness)
		{
			StringifiedArray += FString::SanitizeFloat(e) + " ";
		}

		PythonComp->CallPythonComponentMethod(FString("ReceivedAllFitness"), StringifiedArray);

	}
	else {
		if (ProcessedAgents % BatchNum ==0 )
			InitializeAgentbatch();
	}
}

void ANE_Handler::InitializeAgentbatch()
{

	for (size_t i = 0; i < BatchNum && ProcessedAgents + (i+1) <= NNNum; i++)
	{
		int index = ProcessedAgents + i;
		FActorSpawnParameters SpawnInfo;
		//ANN_ControlledPawn* Agent = GetWorld()->SpawnActor<ANN_ControlledPawn>(NNAgent, GetActorLocation(), GetActorRotation(), SpawnInfo);
		//ANN_ControlledPawn* Agent = Cast< ANN_ControlledPawn>(PythonComp->CallPythonComponentMethodObject("SpawnModel",nullptr));
		PythonComp->CallPythonComponentMethod(FString("SpawnNLoadModelFromIndex"), FString::FromInt(index));
	}


}

