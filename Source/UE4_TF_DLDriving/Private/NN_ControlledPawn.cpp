// Fill out your copyright notice in the Description page of Project Settings.


#include "NN_ControlledPawn.h"
#include "Engine/Engine.h"
#include "DrawDebugHelpers.h"
#include "WheeledVehicleMovementComponent4W.h"
#include "Components/SkeletalMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "PythonComponent.h"
#include "AIController.h"
#include "Components/PrimitiveComponent.h"
#include "Engine/EngineTypes.h"
#include "NE_Handler.h"

ANN_ControlledPawn::ANN_ControlledPawn()
{
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> NNMaterial(TEXT("/Game/VehicleAdv/Materials/MaterialInstances/Template_BaseOrange.Template_BaseOrange"));
	GetMesh()->SetMaterial(0, NNMaterial.Object);
	GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Vehicle, ECollisionResponse::ECR_Ignore);
	MaxRaycastLengthFront = MaxRaycastLengthSide = 1000.f;
	
	PythonComp = CreateDefaultSubobject<UPythonComponent>(TEXT("PyComponent"));
	PythonComp->PythonModule = PythonComp->PythonClass = "NNDriveCar";

	GetMesh()->OnComponentHit.AddDynamic(this, &ANN_ControlledPawn::OnHit);
	OnActorBeginOverlap.AddDynamic(this, &ANN_ControlledPawn::OverlapHandler);

	//TArray<FName> Names;
	//GetMesh()->GetBoneNames(Names);
	ShortestLapTime = 20.f;
	//AgentIndex = -1;
	//OnEndPlay.AddDynamic(this, &ANN_ControlledPawn::EndPlayHandler);
	MinVelocityThreshold = 2.5;
	MaxLifetimeLowVelocity = 3;
	MaxLifetime = 40;
}

void ANN_ControlledPawn::SetupPlayerInputComponent(UInputComponent* InpCmp)
{
	if(bEnablePlayerInput)
		Super::SetupPlayerInputComponent(InpCmp);
	else
		AWheeledVehicle::SetupPlayerInputComponent(InpCmp);
}

void ANN_ControlledPawn::OverlapHandler(AActor* OverlappedActor, AActor* OtherActor)
{
	//Agent reaches the end line
	if (!OtherActor->GetName().Compare(FString("FinishLine"))) {
		int AgentIndex = PythonComp->CallPythonComponentMethodInt(FString("GetIndex"), FString());
		if (AgentIndex >= 0) {
			Cast<ANE_Handler>(GetOwner())->OnAgentFitnessComputed.Broadcast(AgentIndex, 9.f * FMath::Exp((-0.2f * GetGameTimeSinceCreation())) + 1.f);
			Destroy();
		}
	}

}

void ANN_ControlledPawn::BeginPlay()
{
	Super::BeginPlay();

	GetMesh()->SetBodyNotifyRigidBodyCollision(true, FName("Vehicle"));

	MainBBox = GetMesh()->Bounds.GetBox();

	AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
	FActorSpawnParameters SpawnInfo;
	AAIController* AIController = GetWorld()->SpawnActor<AAIController>(FVector::ZeroVector, FRotator::ZeroRotator,SpawnInfo);
	AIController->Possess(this);

}

float ANN_ControlledPawn::GetFrontDstPerc()
{
	FHitResult OutHit;
	FBox BBox = MainBBox;
	FCollisionQueryParams CollisionParams;
	CollisionParams.bTraceComplex = true;
	CollisionParams.AddIgnoredComponent(GetMesh());

	FVector ForwardVector = GetActorForwardVector();
	ForwardVector.Z = 0.0f;
	ForwardVector.Normalize();
	FVector Location = GetActorLocation()+ InternalCameraOrigin.Z* FVector(0,0,1);
	FVector Start = ((ForwardVector * (BBox.GetExtent().X+2.5f)) + Location);
	FVector End = ((ForwardVector * MaxRaycastLengthFront) + Start);

	float percDst = 0.0;


	DrawDebugLine(GetWorld(), Start, End, FColor::Red, false, -1, 0, 5);
	if (GetWorld()->LineTraceSingleByChannel(OutHit, Start, End, ECollisionChannel::ECC_Vehicle, CollisionParams))
	{
		if (OutHit.bBlockingHit && OutHit.GetActor())
		{
			percDst = OutHit.Distance / FVector::Distance(Start,End);
			
			if (GEngine) {

				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("You are hitting: %s"), *OutHit.GetActor()->GetName()));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("Impact Point: %s"), *FString::SanitizeFloat(OutHit.Distance)));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("Front Perc: %s"), *FString::SanitizeFloat(percDst)));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("Comp: %s"), *(End-Start).ToString()));
			}
		}
	}
	return percDst;
}

void ANN_ControlledPawn::OnHit(UPrimitiveComponent* HitComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, FVector NormalImpulse, const FHitResult& Hit)
{
	if (GEngine) {

		//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("Comp: %s %s %s"), *Hit.BoneName.ToString(), *Hit.MyBoneName.ToString(), *HitComponent->GetName()));

	}
	//NOTIFY PYTHON OF YOUR SCORE
	//Agent hits a wall
	int AgentIndex = PythonComp->CallPythonComponentMethodInt(FString("GetIndex"), FString());
	if (AgentIndex >= 0) {
		Cast<ANE_Handler>(GetOwner())->OnAgentFitnessComputed.Broadcast(AgentIndex, FitnessFunction(GetGameTimeSinceCreation()));
		Destroy();
	}
}

float ANN_ControlledPawn::GetSideTrackPerc()
{
	FHitResult OutHit;
	FBox BBox = MainBBox;
	FCollisionQueryParams CollisionParams;
	CollisionParams.bTraceComplex = true;
	CollisionParams.AddIgnoredComponent(GetMesh());

	FHitResult OutHitRight;
	FHitResult OutHitLeft;
	FVector RightVector = GetActorRightVector();
	RightVector.Z = 0.0f;
	RightVector.Normalize();
	FVector Location = GetActorLocation() + InternalCameraOrigin.Z * FVector(0, 0, 1);
	FVector StartRight = ((RightVector * (BBox.GetExtent().Y + 3.f)) + Location);
	FVector EndRight = ((RightVector * MaxRaycastLengthSide) + StartRight);

	FVector StartLeft = (-(RightVector * (BBox.GetExtent().Y + 3.f)) + Location);
	FVector EndLeft = (-(RightVector * MaxRaycastLengthSide) + StartLeft);


	float percDst = 0.0;

	DrawDebugLine(GetWorld(), StartRight, EndRight, FColor::Yellow, false, -1, 0, 5);
	DrawDebugLine(GetWorld(), StartLeft, EndLeft, FColor::Green, false, -1, 0, 5);

	if (GetWorld()->LineTraceSingleByChannel(OutHitRight, StartRight, EndRight, ECollisionChannel::ECC_Vehicle, CollisionParams) && GetWorld()->LineTraceSingleByChannel(OutHitLeft, StartLeft, EndLeft, ECollisionChannel::ECC_Vehicle, CollisionParams))
	{
		if (OutHitRight.bBlockingHit && OutHitRight.GetActor() && OutHitLeft.bBlockingHit && OutHitLeft.GetActor())
		{
			percDst = -1 + (OutHitLeft.Distance / ((OutHitLeft.Distance + OutHitRight.Distance) / 2));
			
			if (GEngine) {
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Yellow, FString::Printf(TEXT("You are hitting: %s"), *OutHitRight.GetActor()->GetName()));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("You are hitting: %s"), *OutHitLeft.GetActor()->GetName()));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("Comp: %s"), *(EndRight - StartRight).ToString()));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("SIDE perc: %s"), *FString::SanitizeFloat(percDst)));

			}
		}
	}

	return percDst;
}

void ANN_ControlledPawn::Tick(float Delta)
{
	Super::Tick(Delta);
	MaxLifetime -= Delta;
	if (GetVehicleMovement()->GetForwardSpeed() * 0.036f < MinVelocityThreshold ) {
		MaxLifetimeLowVelocity -= Delta;
	}

	if (MaxLifetime < 0) {
		
		int AgentIndex = PythonComp->CallPythonComponentMethodInt(FString("GetIndex"), FString());
		if (AgentIndex >= 0) {
			Cast<ANE_Handler>(GetOwner())->OnAgentFitnessComputed.Broadcast(AgentIndex, FitnessFunction(GetGameTimeSinceCreation()));
			Destroy();
		}

	}

	if (MaxLifetimeLowVelocity < 0) {
		//Agent is too slow
		int AgentIndex = PythonComp->CallPythonComponentMethodInt(FString("GetIndex"), FString());
		if (AgentIndex >= 0) {
			Cast<ANE_Handler>(GetOwner())->OnAgentFitnessComputed.Broadcast(AgentIndex, -1.f);
			Destroy();
		}

	}

	/*SENSORS-RAYCASTS*/
	//DrawDebugLine(GetWorld(), GetActorLocation(), GetActorLocation()+ 100 *GetActorForwardVector(), FColor::White, false, -1, 0, 5);
	/*if (GEngine) {
		FVector Fwd = GetActorForwardVector() * FVector(1,1,1);
		FVector Rig = GetActorRightVector() * FVector(1, 1, 1);

		GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("Comp: %s %s"), *Fwd.ToString(), *Rig.ToString()));

	}*/
	//GetInputsAsString();
	/*@TODO: SEND INPUT TO PYTHON NN*/
	
}

/*USE PYTHON OUTPUT*/
void ANN_ControlledPawn::ActuateActions(float forward, float right)
{
	MoveForward(forward);
	MoveRight(right);
}


FString ANN_ControlledPawn::GetInputsAsString()
{
	float KPH = GetVehicleMovement()->GetForwardSpeed() * 0.036f;
	return FString(FString::SanitizeFloat(KPH/94.f)+" "+ FString::SanitizeFloat(GetFrontDstPerc())+" "+ FString::SanitizeFloat(GetSideTrackPerc()));
}

float ANN_ControlledPawn::FitnessFunction(float x)
{
	return x/MaxLifetime;//1/FMath::Exp(ShortestLapTime - x);
}