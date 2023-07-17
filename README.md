# UE4_TF_DLDriving
Starting from the VehicleAdvanced template of Unreal, this project aims to teach a car to race in a circuit using different AI techniques exploiting the Python plugin for UE4.

## Disclaimer
The Unreal Engine version used is 4.23 since it is the latest supported by the plugin (https://github.com/20tab/UnrealEnginePython). 
You can download the whole project (including the embedded Python VM) from the release section of this project.
If you download this project from the master, you have to manually import each plugin using the release of (https://github.com/getnamo/tensorflow-ue4/releases) or (https://github.com/20tab/UnrealEnginePython/releases).

## Project Status
Up to now, a basic Neuroevolution algorithm has been successfully implemented and all the most performant agents have been tested on unseen tracks with good results.
The agents can race on a given circuit without going off the tracks: all of them use a simple Neural Net with all the design and computation parts implemented completely using the Machine Learning library TensorFlow 2.5.0.
</br>
<p align="center">
<img src="https://raw.githubusercontent.com/pikumb94/UE4_TF_DLDriving/master/Resources/Track1.gif" width="307" height="169" />&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/pikumb94/UE4_TF_DLDriving/master/Resources/Track2.gif" width="269" height="169" />&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/pikumb94/UE4_TF_DLDriving/master/Resources/Track3.gif" width="200" height="169" />
<p align="center">
<sub><em>The result of a batch of 15 agents at the tenth generation in tracks of increasing difficulty during Neuroevolution. 
</br>In this generation the agents learn to avoid going backwards.</em></sub>
</p>
</p>

</br>
<p align="center">
<img src="https://raw.githubusercontent.com/pikumb94/UE4_TF_DLDriving/master/Resources/TrackTest.gif" width="400" height="400" />
<p align="center">
<sub><em>Testing the best models found during the Neuroevolution algorithm using the three tracks shown before. The agents are tested using an unseen and irregular track: as expected, the agents found with simple tracks will hit the barriers very soon, while the ones that learned from complex tracks will survive and behave as intended (i.e. complete the lap without hitting any wall).</em></sub>
</p>
</p>

## Future Developments
Since Phyton can be used, there are a lot of libraries that can be used and so a lot of techniques and improvements for this project:
* Change the fitness function in the Neuroevolution framework implemented in order to obtain a better performant agent.
* NEAT approach using NEAT-Python library
* Reinforcement Learning approach using KerasRL
* Supervised Learning approach using TF library
