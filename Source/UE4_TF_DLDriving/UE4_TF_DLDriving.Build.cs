// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class UE4_TF_DLDriving : ModuleRules
{
	public UE4_TF_DLDriving(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "PhysXVehicles", "HeadMountedDisplay", "UnrealEnginePython" });

		PublicDefinitions.Add("HMD_MODULE_INCLUDED=1");
	}
}
