from mesa import Agent;
from mesa.datacollection import DataCollector
'''
#Tumor cells class
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
        
    '''
    # STEP METHOD ()
    ### Description:
    Define behaviour for diff situations here.
    '''
    def step(self):
        #When Apoptosis
        
        pass
    #APOPTOSIS METHOD:
    def apoptosis(self): # Försöka modellera om cellen är tillräckligt nära en anti-cancer-makrofag så dödas den mha. denna metod
            self.viable = False
    #PROLIFERATION METHOD
    def proliferate(self):
         adjacent_grid_cells = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]

         valid_grid_cells = []; #Save Identified empty grid cells here. 



         

# Imports all the required classes from the needed modules for creating the Mesa-model

                    # Add the type of cell as an additional instance variable

        # OBS: Lägg till flera relevanta instansvariabler!!

    # Exempel på resterande metoder som tumörcellen kommer att behöva 
    #def step():

    #def migration():

    #def proliferation():
    
    #def resistance_Macrohpage():