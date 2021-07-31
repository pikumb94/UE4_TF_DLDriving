import unreal_engine as ue
import tensorflow as tf
from tensorflow.python.keras import backend as ks#to ensure things work well with multi-threading
import numpy as np   #for reshaping input
import json
from json import JSONEncoder
from unreal_engine.classes import WheeledVehicleMovementComponent
from unreal_engine.classes import NE_Handler
from unreal_engine import FVector, FRotator, FTransform, FHitResult
from unreal_engine.classes import ActorComponent, PythonComponent
from collections.abc import Iterable
import pathlib



def Flatten(NN):
  fl_weights = NN
  v=np.empty()
  for wsNbs in fl_weights:
    if(isinstance(wsNbs, Iterable)):#??
      for wsOb in wsNbs:
        if(isinstance(wsOb, Iterable)):
          for ws in wsOb:
            #type(ws)
            np.append(v,ws)
        else:
          #type(wsOb)
          np.append(v,wsOb)
    else:
      np.append(v,wsNbs)
  return v

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

def RecAssignLinearToStructured(StructuredVector,FlattenedVector,pivot):
  if(isinstance(StructuredVector, Iterable)):
    if(len(StructuredVector)):
      if(not isinstance(StructuredVector[0], Iterable)):
        length = len(StructuredVector)
        for cnt in range(length):
          #print(len(FlattenedVector))

          StructuredVector[cnt] = FlattenedVector[pivot]
          pivot+=1
        return pivot
      else:
        max_pivot=max(0,pivot)
        for Struct in StructuredVector:
          max_pivot = max(RecAssignLinearToStructured(Struct,FlattenedVector,max_pivot),max_pivot)
        return max_pivot     
    else:
      return pivot
  else:
    StructuredVector = FlattenedVector[pivot]
    pivot+=1
    return pivot

def DeFlattenWTopology(NN,FlattenedWeights):
  #print(FlattenedWeights)
  #print(type(FlattenedWeights))
  v= NN.get_weights()
  RecAssignLinearToStructured(v,FlattenedWeights,0)
  return v

def Two_Point_Crossover(Ws_NN1,Ws_NN2):
  v1=RecFlatten(Ws_NN1)
  v2=RecFlatten(Ws_NN2)

  p1=np.random.randint(0, v1.size)
  p2=np.random.randint(0, v2.size)
  c1=c2 =None

  if(p1<p2):
    c1=np.concatenate((v1[:p1],v2[p1:p2],v1[p2:]))
    c2=np.concatenate((v2[:p1],v1[p1:p2],v2[p2:]))
  else:
    c1=np.concatenate((v1[:p2],v2[p2:p1],v1[p1:]))
    c2=np.concatenate((v2[:p2],v1[p2:p1],v2[p1:]))

  return [c1,c2]

def N_Point_Crossover(Ws_NN1,Ws_NN2):
  v1=RecFlatten(Ws_NN1)
  v2=RecFlatten(Ws_NN2)
  c1=v1
  c2=v2
  for i in range(0,int(v1.size/2)):
    tmp = c1[i*2]
    c1[i*2] = c2[i*2]
    c2[i*2] = tmp

  return [c1,c2]

def Tournament_Selection(NNs,k):
  BestParent = NNs[np.random.randint(0, len(NNs))]
  for i in range(int(k-1)):
    Parent = NNs[np.random.randint(0, len(NNs))]
    if Parent[1]>BestParent[1]:
      BestParent = Parent  
  return BestParent

def Mutate(Weights,pM):
    length = len(Weights)
    #print(length)
    for i in range(length):
      if np.random.binomial(1, pM, 1)[0] == 1:
         Weights[i] = Weights[i]+np.random.normal()#np.random.normal(scale=1.5)
    
    return Weights

def reset_weights(model):
  session = ks.get_session()
  for layer in model.layers: 
      for v in layer.__dict__:
          v_arg = getattr(layer,v)
          if hasattr(v_arg,'initializer'):
              initializer_method = getattr(v_arg, 'initializer')
              initializer_method.run(session=session)

def scatter_weights(model,M):
  v=RecFlatten(model.get_weights())
  vM = Mutate(v,M)
  return DeFlattenWTopology(model,vM)

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

#@title Testo del titolo predefinito
#Define the NN
ks.clear_session()
print('NEHandler')

#Evolution Part|| Data: N: number of generations, S: population size, E: elitism rate, C: crossover rate, M: mutation rate; K: percentage of ways in tournament selection
N=100           #100
S=30           #50
E=0.5          #0.5
C=0.8          #0.6
M=0.35         #0.1
K=0.2         #0.25

NN_topology = [tf.keras.layers.Dense(3, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(4, activation=tf.nn.tanh),
tf.keras.layers.Dense(2, activation=tf.nn.tanh)]

NNs_Population=[]

class NEHandler:

  def __init__(self):
    global NNs_Population
    self.NESteps=0
    ks.clear_session()
    self.NNmodel = tf.keras.models.Sequential(NN_topology)
    y=self.NNmodel(tf.zeros((1, 3)))
    
    self.BestFitness=0
    self.BestModel = self.NNmodel.get_weights()
    
  def get_PopulationSize(self):
    return len(NNs_Population)
    
  def begin_play(self):    
    for i in range(S):
      ks.clear_session()
      model = tf.keras.models.clone_model(self.NNmodel)
      x = tf.zeros((1, 3))
      y = model(x)
            
      NNs_Population.append((scatter_weights(model,.75),.0))#Initialize with random fitness
    self.RequestComputeAllFitness()

  def RequestComputeAllFitness(self):
    global NNs_Population
    #print('RequestComputeAllFitness')
    NNs_lenght = len(NNs_Population)
    self.uobject.GetOwner().broadcast('OnStartFitnessComputation')
    #print(self.uobject.GetOwner().functions())
    #self.uobject.GetOwner().StartFitnessComputation.Broadcast()

    #INVOKE AN EVENT ON UNREAL ACTOR=> pass the length of NNs and it decides how to compute it (batch size)!

  def ReceivedAllFitness(self, StringifiedFitnesses):#UE4 ha computato tutte le fitness!
    global NNs_Population
    #decode result from UE4: is a JSON with each element a fitness value!
    #print('ReceivedAllFitness')
    BatchFitnesses = [float(x) for x in StringifiedFitnesses.split()]
    BF_lenght = len(BatchFitnesses)
    NNs_lenght = len(NNs_Population)
    #print(NNs_lenght)
    for i in range(0, NNs_lenght):
      new_tuple = (NNs_Population[i][0],BatchFitnesses[i])
      NNs_Population[i]=new_tuple#TODO: evaluate fitness for all current population
    NNs_Population.sort(key=lambda x: x[1], reverse=True)
    self.ExecuteNeuroevolutionStep()

  def getWeigthsInPopulation(self,index):
    return NNs_Population[index][0]
    
  def SpawnNLoadModelFromIndex(self,index):
        new_actor = self.uobject.actor_spawn(ue.find_class('NN_ControlledPawn'), self.uobject.get_actor_location(),self.uobject.get_actor_rotation())
        new_actor.SetOwner(self.uobject.GetOwner())
        component = new_actor.GetComponentByClass(PythonComponent)

        WeightsIndex = NNs_Population[int(index)][0]
        encodedNumpyData = json.dumps(WeightsIndex, cls=NumpyArrayEncoder)  # use dump() to write array into file
        component.CallPythonComponentMethod("SetIndex", index)
        component.CallPythonComponentMethod("LoadModel", encodedNumpyData)

  def ExecuteNeuroevolutionStep(self):
    global NNs_Population
    #print('ExecuteNeuroevolutionStep')
    if(NNs_Population[0][1] > self.BestFitness):
      self.BestModel = NNs_Population[0][0]
      self.BestFitness = NNs_Population[0][1]
    
    print(f"Generation: {self.NESteps}")
    if(self.NESteps<N):
        NNs_Population = NNs_Population[:int(E*S)]#Survivor selection: apply elitism
        for i in range(0, len(NNs_Population)):
          print(NNs_Population[i][1])
        
        for j in range(0, int(C*S)):
          FatherNN = Tournament_Selection(NNs_Population,K*S)
          MotherNN = Tournament_Selection(NNs_Population,K*S)
          
          ChildrenWeights=[]
          if(j%2==0):
            ChildrenWeights = Two_Point_Crossover(FatherNN[0],MotherNN[0])#Crossover
          else:
            ChildrenWeights = N_Point_Crossover(FatherNN[0],MotherNN[0])#Crossover
          ChildrenWeights = (Mutate(ChildrenWeights[0],M),Mutate(ChildrenWeights[1],M))#Mutation with probability M

          Child1 = DeFlattenWTopology(self.NNmodel,ChildrenWeights[0])
          Child2 = DeFlattenWTopology(self.NNmodel,ChildrenWeights[1])
          NNs_Population.append((Child1,-1))
          NNs_Population.append((Child2,-1))
        self.NESteps= self.NESteps+1
        #print("-----------")
        #for i in range(0, len(NNs_Population)):
        #  print(NNs_Population[i][1])
        self.RequestComputeAllFitness()
        
    else:
      print(self.BestModel)
      print(self.BestFitness)
      for i in range(0, len(NNs_Population)):
        print(NNs_Population[i][0])
        print(NNs_Population[i][1])
        
      Wpath = pathlib.Path(__file__).parent.resolve() 
      path = str(Wpath) + '/Model'
      self.NNmodel.set_weights(self.BestModel)
      self.NNmodel.save_weights(path+'Best')
      
      self.NNmodel.set_weights(NNs_Population[0][0])
      self.NNmodel.save_weights(path+'1')
      self.NNmodel.set_weights(NNs_Population[1][0])
      self.NNmodel.save_weights(path+'2')
      self.NNmodel.set_weights(NNs_Population[2][0])
      self.NNmodel.save_weights(path+'3')
      self.NNmodel.set_weights(NNs_Population[3][0])
      self.NNmodel.save_weights(path+'4')
      self.NNmodel.set_weights(NNs_Population[4][0])
      self.NNmodel.save_weights(path+'5')
      print('Finito!')