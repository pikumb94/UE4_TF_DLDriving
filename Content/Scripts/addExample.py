import json
from pathlib import Path

from tensorflow.python import keras
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Dropout, Flatten
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.models import model_from_json
from tensorflow.python.keras import backend as K
import numpy as np
import operator
import sys
import random

import tensorflow as tf
import unreal_engine as ue
from TFPluginAPI import TFPluginAPI
ue.log('Hello i am a TF SCRIPT')
class ExampleAPI(TFPluginAPI):

    #expected optional api: setup your model for training
    def onSetup(self):
        self.sess = tf.InteractiveSession()
        #self.graph = tf.get_default_graph()
        ue.log('Begin Play on TF SCRIPT')
        self.a = tf.placeholder(tf.float32)
        self.b = tf.placeholder(tf.float32)

        #operation
        self.c = self.a + self.b
        pass
        
    #expected optional api: parse input object and return a result object, which will be converted to json for UE4
    def onJsonInput(self, jsonInput):
        
        print(jsonInput)

        feed_dict = {self.a: jsonInput['a'], self.b: jsonInput['b']}

        rawResult = self.sess.run(self.c,feed_dict)

        return {'c':rawResult.tolist()}

    #custom function to change the op
    def changeOperation(self, type):
        if(type == '+'):
            self.c = self.a + self.b

        elif(type == '-'):
            self.c = self.a - self.b


     #expected optional api: start training your network
    def onBeginTraining(self):
        pass
    
#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def getApi():
    #return CLASSNAME.getInstance()
    return ExampleAPI.getInstance()