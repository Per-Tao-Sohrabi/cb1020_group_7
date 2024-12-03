from mesa import Agent;
'''
# Cells class
### Description:
Objects of the Cells class can be cancerous or non-cancerous.
Cancerous cells have the possibility of inducing endothelial growth from the nearest endothelial cell towards the direction of the cancer cell. 
These cells might also only be cancerous. To be decided.
'''
class Tumor_cells(Agent): 
    #Constructor
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model);
        self.unique_id = unique_id
        self.cancerous = True                           # All the relevant properties (instance variables) for the tumor cell are initiated 
        self.viable = True
        self.proliferation_prob = 0.0846
        self.migration_prob = 0.1167
        self.death_prob = 0.00284
        self.initial_resist_M1_prob = 0
        self.resistance_M1_prob = 0.004
        #location

        #cancerous state

    #Growth method
    def step(self):
        #define behaviour for diff situations here
        pass
# Imports all the required classes from the needed modules for creating the Mesa-model
import numpy as np; import random 
from mesa import Agent, Model
from mesa.time import RandomActivation; from mesa.space import MultiGrid; from mesa.datacollection import DataCollector



class TU_Cell_Agent(Agent):
    def __init__(self, agent_id, model, cell_type):
        super.__init__(agent_id, model)                 # "Super" inherit the parent class's (Agent) instance variables
        self.cell_type = cell_type                      # Add the type of cell as an additional instance variable


class Tumor_cell(TU_Cell_Agent):
    def __init__(self, agent_id, model, TU_cell):
 
        # OBS: Lägg till flera relevanta instansvariabler!!
    
    def apoptosis(): # Försöka modellera om cellen är tillräckligt nära en anti-cancer-makrofag så dödas den mha. denna metod
        if agent_id == abs(): 
            self.viable = False
        else: 
            None

    # Exempel på resterande metoder som tumörcellen kommer att behöva 
    #def step():

    #def migration():

    #def proliferation():
    
    #def resistance_Macrohpage():


