# UE4_TF_DLDriving
Starting from the VehicleAdvanced template of Unreal, this project aims to learn a car to race in a circuit using different AI techniques exploiting TensorFlow plugin for UE4.
##Disclaimer
The Unreal Engine version used is the 4.23 since is the latest supported by the plugin (https://github.com/20tab/UnrealEnginePython). 
The Python VM is embedded in the project and you can find it in the release version of this project
##Project Status
Up to now a basic Neuroevolution algorithm has been successfully implemented and all the most performant agents has been tested on unseen tracks with good result.
The agents can race a given circuit without going off the tracks: all of them uses a simple Neural Net with all the design and computation part implemented completely using the Machine Learning library TensorFlow 2.5.0.

##Future Developments
Since Phyton can be used, there are a lot of libraries that can be used and a lot of techniques and improvements for this project:
* Change the fitness function in the Neuroevolution framework implemented in order to obtain a better performant agent.
* NEAT approach using NEAT-Python library
* Reinforcement Learning approach using KerasRL
* Supervised Learning approach using TF library
