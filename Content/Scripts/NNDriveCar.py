import unreal_engine as ue
import tensorflow as tf
from tensorflow.python.keras import backend as ks	#to ensure things work well with multi-threading
import numpy as np   	#for reshaping input
import json
import operator      	#used for getting max prediction from 1x10 output array

from collections.abc import Iterable   # import directly from collections for Python < 3.3

from unreal_engine.classes import WheeledVehicleMovementComponent

print('NNDriveCar')
NN_topology = [tf.keras.layers.Dense(3, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(2, activation=tf.nn.tanh)]
#sess = ks.get_session()

class NNDriveCar:


    def __init__(self):
    #model and topology is set statically to avoid to pass the topology for every NNCar spawned
        self.model = tf.keras.models.Sequential(NN_topology)
        self.model(tf.constant([[1.0,1.0,1.0]]))
        self.bModelLoaded = False
        self.bTopologyLoaded = True
        
    # this is called on game start
    def begin_play(self):
        #sess = tf.Session()
        self.pawn = self.uobject.get_owner()
        #print(self.uobject.functions())
        #print(self.uobject.properties())
        self.uobject.SetComponentTickInterval(0.150)
        #print(self.pawn.properties())
        #print(self.pawn.functions())
        
    # this is called at every 'tick'    
    def tick(self, delta_time):
        #print(delta_time)
        if(self.bModelLoaded):
            x=tf.compat.v1.placeholder(tf.float32, shape=(1, 3))
            #y = self.model()#velocity, front and side
            y=self.model(x)
            with ks.get_session() as session:
                result = session.run(y, feed_dict={x: [[1.0,-1.0,1.0]]})
                print(result)
                self.pawn.ActuateActions(1.0,1.0)

    
    def LoadModel(self, NewModel):
        decodedWeights = json.loads(NewModel)
        self.model.set_weights([np.array(x) for x in decodedWeights])
        self.bModelLoaded = True
        print('Model Loaded:')
        print(self.model.get_weights())
        
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