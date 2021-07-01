import unreal_engine as ue
import tensorflow as tf
from tensorflow.python.keras import backend as ks	#to ensure things work well with multi-threading
import numpy as np   	#for reshaping input
import json
from json import JSONEncoder
from unreal_engine.classes import WheeledVehicleMovementComponent
#from unreal_engine.classes import NN_ControlledPawn
from unreal_engine import FVector, FRotator, FTransform, FHitResult
from unreal_engine.classes import ActorComponent, PythonComponent
from collections.abc import Iterable

ks.clear_session()
print('TestNE')
print(tf.version.VERSION)
NN_topology = [tf.keras.layers.Dense(3, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(2, activation=tf.nn.tanh)]

model = tf.keras.models.Sequential(NN_topology)
x = tf.constant([[1.0,-1.0,1.0]])
y = model(x)
#new_actor = None

class TestNE:
    def __init__(self):
        self.time=0
        self.triggered = False
    # this is called on game start
    def begin_play(self):
        time=0
    
    def tick(self, delta_time):
        # get current location
        self.time = self.time+delta_time
        location = self.uobject.get_actor_location()
        if( (not self.triggered) and self.time >= 2.0):
            print('TRIGGER')
            self.triggered = True
            self.you_pressed_K()
            self.you_pressed_K()
            self.you_pressed_K()
        
    
    def speak(self, words):
        ue.log(words)
    
    def you_pressed_K(self):
        ue.log_warning('SPAWNING')
        new_actor = self.uobject.actor_spawn(ue.find_class('NN_ControlledPawn'), self.uobject.get_actor_location(),FRotator(0, 0, 0))
        component = new_actor.GetComponentByClass(PythonComponent)
        
        #print(model.get_weights())
        encodedNumpyData = json.dumps(model.get_weights(), cls=NumpyArrayEncoder)  # use dump() to write array into file
        component.CallPythonComponentMethod("LoadModel", encodedNumpyData)
        #print(component.functions())









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