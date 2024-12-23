from mesa import Agent;
from mesa.datacollection import DataCollector
import random

'''
#Tumor cells class
### Description:
Objects of the Cells class can be cancerous or non-cancerous.
Cancerous cells have the possibility of inducing endothelial growth from the nearest endothelial cell towards the direction of the cancer cell. 
These cells might also only be cancerous. To be decided.
'''
class Tumor_cells(Agent): 
    #Constructor
    def __init__(self, unique_id, position, model): #Position inputed as (x,y)
        super().__init__(unique_id, model);
        self.model = model;
        self.unique_id = unique_id;
        self.position = position;
        self.viable = True

        self.cancerous = True     
        # All the relevant properties (instance variables) for the tumor cell are initiated 

        self.proliferation_prob = 0.0846
        self.migration_prob = 0.1167
        self.death_prob = 0.00284
        self.initial_resist_M1_prob = 0
        self.resistance_M1_prob = 0.004
    
    #SETTERS
    def set_death_prob(self, number):
         self.death_prob = number
         
    #STEP
    def step(self):
        '''
        #ENDOTHELIAL-TUMOR_CELL INTERACTION:
        #1. Identify nearest endo obj
        nearest_endo_obj, distance = self.identify_nearest_endo_obj()


        #NORMAL TUMOR CELL LIFE CYCLE BEHAVIOUR
        #Then check self induced states
        '''
        if random.randint(0,100) < 100*self.proliferation_prob:
            self.proliferate();
        if random.randint(0,100) < 100*self.death_prob:
            self.apoptosis()


        #if adjacent or diagonal cell contain(fibroblast) do Increase  * death_prob?
        #if cell_M.._dist < critDistToM:do Proliferation in empty cell * prolifiration_prob;
        #if cell_endo_dist > critDistHypoxia:Induce Endothelial Proliferation;

    #IDENTIFY NEAREST ENDO. CELL OBJ. 
    def identify_nearest_endo_obj(self):
         nearest_endo_obj = None
         distance = None
         return nearest_endo_obj, distance
    
    #APOPTOSIS METHOD:
    def apoptosis(self): # Försöka modellera om cellen är tillräckligt nära en anti-cancer-makrofag så dödas den mha. denna metod
            self.viable = False
            self.model.grid.remove_agent(self);
            self.model.schedule.remove(self);

    #PROLIFERATION METHOD
    def proliferate(self):
         try:
            self.model.generate_agents(Tumor_cells, "proliferate", 1, self.position); #will be changed to proliferate
            print("Tumor cell generated, id = ", self.unique_id);
         except Exception as e:
              print(f"Error while generating Tumor cell from agent  {self.unique_id} {e}")



    

    
# Imports all the required classes from the needed modules for creating the Mesa-model
                    # Add the type of cell as an additional instance variable
        # OBS: Lägg till flera relevanta instansvariabler!!
    # Exempel på resterande metoder som tumörcellen kommer att behöva 
    #def step():
    #def migration():
    #def proliferation():
    #def resistance_Macrohpage():