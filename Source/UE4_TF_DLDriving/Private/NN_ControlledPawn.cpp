// Fill out your copyright notice in the Description page of Project Settings.


#include "NN_ControlledPawn.h"
#include "Engine/Engine.h"
#include "DrawDebugHelpers.h"
#include "WheeledVehicleMovementComponent4W.h"
#include "Components/SkeletalMeshComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "PythonComponent.h"
#include "AIController.h"

ANN_ControlledPawn::ANN_ControlledPawn()
{
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> NNMaterial(TEXT("/Game/VehicleAdv/Materials/MaterialInstances/Template_BaseOrange.Template_BaseOrange"));
	GetMesh()->SetMaterial(0, NNMaterial.Object);
	MaxRaycastLengthFront = MaxRaycastLengthSide = 500.f;

	PythonComp = CreateDefaultSubobject<UPythonComponent>(TEXT("PyComponent"));
	PythonComp->PythonModule = PythonComp->PythonClass = "NNDriveCar";
}

void ANN_ControlledPawn::SetupPlayerInputComponent(UInputComponent* InpCmp)
{
	if(bEnablePlayerInput)
		Super::SetupPlayerInputComponent(InpCmp);
	else
		AWheeledVehicle::SetupPlayerInputComponent(InpCmp);
}

void ANN_ControlledPawn::BeginPlay()
{
	Super::BeginPlay();

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
	FVector Start = ((ForwardVector * BBox.GetExtent().X) + GetActorLocation());
	FVector End = ((ForwardVector * MaxRaycastLengthFront) + Start);

	float percDst = 0.0;


	DrawDebugLine(GetWorld(), Start, End, FColor::Red, false, -1, 0, 5);
	if (GetWorld()->LineTraceSingleByChannel(OutHit, Start, End, ECC_Visibility, CollisionParams))
	{
		if (OutHit.bBlockingHit && OutHit.GetActor())
		{
			percDst = OutHit.Distance / MaxRaycastLengthFront;

			if (GEngine) {

				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("You are hitting: %s"), *OutHit.GetActor()->GetName()));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("Impact Point: %s"), *FString::SanitizeFloat(OutHit.Distance)));
				//GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Red, FString::Printf(TEXT("Front Perc: %s"), *FString::SanitizeFloat(percDst)));

			}
		}
	}
	return percDst;
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
	FVector StartRight = ((RightVector * BBox.GetExtent().Y) + GetActorLocation());
	FVector EndRight = ((RightVector * MaxRaycastLengthSide) + StartRight);

	FVector StartLeft = (-(RightVector * BBox.GetExtent().Y) + GetActorLocation());
	FVector EndLeft = (-(RightVector * MaxRaycastLengthSide) + StartLeft);


	float percDst = 0.0;

	DrawDebugLine(GetWorld(), StartRight, EndRight, FColor::Yellow, false, -1, 0, 5);
	DrawDebugLine(GetWorld(), StartLeft, EndLeft, FColor::Green, false, -1, 0, 5);

	if (GetWorld()->LineTraceSingleByChannel(OutHitRight, StartRight, EndRight, ECC_Visibility, CollisionParams) && GetWorld()->LineTraceSingleByChannel(OutHitLeft, StartLeft, EndLeft, ECC_Visibility, CollisionParams))
	{
		if (OutHitRight.bBlockingHit && OutHitRight.GetActor() && OutHitLeft.bBlockingHit && OutHitLeft.GetActor())
		{
			percDst = -1 + (OutHitLeft.Distance / ((OutHitLeft.Distance + OutHitRight.Distance) / 2));

			if (GEngine) {

				GEngine->AddOnScreenDebugMessage(-1, 1.f, FColor::Green, FString::Printf(TEXT("SIDE perc: %s"), *FString::SanitizeFloat(percDst)));

			}
		}
	}

	return percDst;
}

void ANN_ControlledPawn::Tick(float Delta)
{
	Super::Tick(Delta);

	/*SENSORS-RAYCASTS*/


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
	return FString(FString::SanitizeFloat(KPH)+" "+ FString::SanitizeFloat(GetFrontDstPerc())+" "+ FString::SanitizeFloat(GetSideTrackPerc()));
}