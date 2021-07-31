import unreal_engine as ue
import tensorflow as tf
from tensorflow.python.keras import backend as ks	#to ensure things work well with multi-threading
from tensorflow import keras
import numpy as np   	#for reshaping input
import json
from json import JSONEncoder
from unreal_engine.classes import WheeledVehicleMovementComponent
#from unreal_engine.classes import NN_ControlledPawn
from unreal_engine import FVector, FRotator, FTransform, FHitResult
from unreal_engine.classes import ActorComponent, PythonComponent
from collections.abc import Iterable
import pathlib

ks.clear_session()
print('TestNE')
NN_topology = [tf.keras.layers.Dense(3, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(2, activation=tf.nn.tanh)]

model = tf.keras.models.Sequential(NN_topology)
x = tf.constant([[1.0,1.0,1.0]])
y = model(x)
#new_actor = None

class NETest:

    def begin_play(self):
      global model
      filename = self.uobject.get_owner().get_name()
      Wpath = pathlib.Path(__file__).parent.resolve() 
      path = str(Wpath) + '/Models/ToTestModels/'+filename
      #path = str(Wpath) + '/'+filename
      model.load_weights(path)
      
      new_actor = self.uobject.actor_spawn(ue.find_class('NN_ControlledPawn'), self.uobject.get_actor_location(),self.uobject.get_actor_rotation())
      #print(new_actor.properties())
      #print(new_actor.functions())
      new_actor.SetActorLabel(filename)
      new_actor.SetOwner(self.uobject.GetOwner())
      component = new_actor.GetComponentByClass(PythonComponent)
      WeightsIndex = model.get_weights()
      print(WeightsIndex)
      encodedNumpyData = json.dumps(WeightsIndex, cls=NumpyArrayEncoder)  # use dump() to write array into file
      component.CallPythonComponentMethod("SetIndex", str(-1))
      component.CallPythonComponentMethod("LoadModel", encodedNumpyData)    
  


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def RecFlatten(Weights):
  v=np.array([])
  if(isinstance(Weights, Iterable)):

    if(len(Weights)):
      if(not isinstance(Weights[0], Iterable)):
        #print(Weights)
        return Weights
      else:
        
        for Ws in Weights:
          v= np.append(v, Ws)
        return v
    else:
      return np.empty([])

  else:
    return np.append(v,Weights)