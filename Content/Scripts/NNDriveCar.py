import unreal_engine as ue
import tensorflow as tf
from tensorflow.python.keras import backend as ks	#to ensure things work well with multi-threading
import numpy as np   	#for reshaping input
import json
import operator      	#used for getting max prediction from 1x10 output array

from collections.abc import Iterable   # import directly from collections for Python < 3.3

from unreal_engine.classes import WheeledVehicleMovementComponent

NN_topology = [tf.keras.layers.Dense(3, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(2, activation=tf.nn.tanh)]

class NNDriveCar:

    def __init__(self):
    #model and topology is set statically to avoid to pass the topology for every NNCar spawned
        self.model = tf.keras.models.Sequential(NN_topology)
        self.model(tf.constant([[0.0,0.0,0.0]]))
        self.bModelLoaded = False
        self.bTopologyLoaded = True
        
    # this is called on game start
    def begin_play(self):
        self.pawn = self.uobject.get_owner()
        self.component = self.uobject.get_component_by_type(WheeledVehicleMovementComponent)
        #print(self.pawn.functions())
        #print(self.uobject.properties())
        #self.uobject.SetComponentTickInterval(0.100)
        #print(self.pawn.properties())
        #print(self.pawn.functions())
        
    # this is called at every 'tick'    
    def tick(self, delta_time):
        SplitStr = self.pawn.GetInputsAsString().split()
        
        if(self.bModelLoaded):
            SplitStr = np.array(SplitStr)
            SplitStr = SplitStr.astype(np.float32)
            x = tf.constant([SplitStr])
            y = self.model(x)
            #print('x:%s y:%s'%(type(x[0][0].numpy()),type(y[0][0].numpy())))
            #print('x:',x[0][0],x[0][1],x[0][2])
            #print('y:',y[0][0],y[0][1])
            #print('x:%s'%(x.numpy()))
            #print('y:%s'%(y.numpy()))
            #self.pawn.ActuateActions(y[0][0],y[0][1])
            self.pawn.ActuateActions(1-max(0.0,y[0][0]),y[0][1])
    
    def SetIndex(self, index):
        self.index = int(index)
    
    def GetIndex(self):
        return self.index
    
    def LoadModel(self, NewModel):
        decodedWeights = json.loads(NewModel)
        self.model.set_weights([np.array(x) for x in decodedWeights])
        self.bModelLoaded = True
        #print('Model Loaded:')
        #print(self.model.get_weights())
        
    def LoadTopology(self, Topology):
        seld.model = ks.models.model_from_json(Topology)
        self.bTopologyLoaded = True

        
    def you_pressed_K(self):
        ue.log_warning('you pressed K')
        component = self.uobject.get_component_by_type(WheeledVehicleMovementComponent)
        #ue.log_warning(component.get_velocity)
        yesno = self.uobject.actor_has_component_of_type(WheeledVehicleMovementComponent)
        #ue.log_warning(self.uobject.get_actor_velocity())
        ue.log_warning(yesno)
        
    def parla(self, words):
        ue.log(words)
    
    def speak(self):
        ue.log('parole')