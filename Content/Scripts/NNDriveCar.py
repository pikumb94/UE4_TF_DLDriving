import unreal_engine as ue
import tensorflow as tf
from tensorflow.python.keras import backend as ks	#to ensure things work well with multi-threading
import numpy as np   	#for reshaping input
import operator      	#used for getting max prediction from 1x10 output array

from collections.abc import Iterable   # import directly from collections for Python < 3.3

from unreal_engine.classes import WheeledVehicleMovementComponent

print('NNDriveCar')

class NNDriveCar:


    def __init__(self):
        self.model=None
        self.bModelLoaded = False
        
    # this is called on game start
    def begin_play(self):
        sess = tf.Session()
        self.pawn = self.uobject.get_owner()
        #print(self.pawn.properties())
        #print(self.pawn.functions())
        
    # this is called at every 'tick'    
    def tick(self, delta_time):
        if(self.bModelLoaded):
            y = model(tf.constant([[1.0,-1.0,1.0]]))#velocity, front and side
            self.pawn.ActuateActions(y.numpy()[0][0],y.numpy()[0][1])
        
    
    def LoadModel(self, NewModel):
        print(NewModel)
        self.model = NewModel
        self.bModelLoaded = True
        print('Model Loaded')

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