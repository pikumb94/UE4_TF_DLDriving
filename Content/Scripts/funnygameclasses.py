import unreal_engine as ue
import tensorflow as tf
from unreal_engine.classes import WheeledVehicleMovementComponent

print('Hello i am a Python module')

class Hero:

    # this is called on game start
    def begin_play(self):
        ue.log('Begin Play on Hero class')
        hello = tf.constant('Hello, TensorFlow!')
        sess = tf.Session()
        print(sess.run(hello))
        
        #self.pawn = self.uobject.get_owner()
        self.uobject.bind_key('K', ue.IE_PRESSED, self.you_pressed_K)
        
    # this is called at every 'tick'    
    def tick(self, delta_time):
        # get current location
        location = self.uobject.get_actor_location()
        # increase Z honouring delta_time
        location.z += 100 * delta_time
        # set new location
        self.uobject.set_actor_location(location)
        
    def speak(self, words):
        ue.log(words)
        
    def you_pressed_K(self):
        ue.log_warning('you pressed K')
        
class Vehicle:
    def begin_play(self):
        print('Begin Play on Vehicle component')
        self.uobject.bind_key('K', ue.IE_PRESSED, self.you_pressed_K)
        
    def changeVar(self):
        uobject.properties()

    def you_pressed_K(self):
        component = self.uobject.get_component_by_type(WheeledVehicleMovementComponent)
        #ue.log_warning(component.get_velocity)
        yesno = self.uobject.actor_has_component_of_type(WheeledVehicleMovementComponent)
        #ue.log_warning(self.uobject.get_actor_velocity())
        ue.log_warning(yesno)
        