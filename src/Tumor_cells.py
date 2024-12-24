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
        # All the relevant properties (instance variables) for the tumor cell are initiated 
        self.proliferation_prob = 0.0846
        self.migration_prob = 0.1167
        self.death_prob = 0.00284
        self.initial_resist_M1_prob = 0
        self.resistance_M1_prob = 0.004
        self.nearest_endo = None;
        self.hypoxia_threshold = 50.0;
    
    #SETTERS
    def set_nearest_endo(self):

        endothelial_agents = self.model.endothelial_list; #endothelial_list is a list containing class type objects as elements.
        counter = 1
        nearest_endo = None
        nearest_dist = None
        for agent in endothelial_agents:
            x_other, y_other = agent.position
            x_self, y_self, = self.position
            distance = ((y_other-y_self)**2 + (x_other-x_self)**2)**(1/2)
            #print("SET!")
            #print(counter)
            #print(f'The distance between tumor_cell {self.unique_id} and endo cell {agent.unique_id} is {distance}')
            if nearest_endo == None:
                nearest_endo = agent
                nearest_dist = distance
            elif nearest_dist > distance:
                nearest_dist = distance
                nearest_endo = agent;
            counter += 1
        print(f'Nearest distance between TC {self.unique_id} and endo {nearest_endo.unique_id} = {nearest_dist}')
        return nearest_endo, nearest_dist
    
    def set_proliferation_prob(self, val):
        self.proliferation_prob = val

    def tumor_endo_interaction(self):
        nearest_endo, nearest_dist = self.set_nearest_endo();
        if nearest_dist < self.hypoxia_threshold:
            self.set_proliferation_prob(0.0864)   #default
        else:
            self.set_proliferation_prob(0.00864)  #0.10 of default
            #Induce proliferation in endothelial cell

            

    #APOPTOSIS METHOD:
    def apoptosis(self): # Försöka modellera om cellen är tillräckligt nära en anti-cancer-makrofag så dödas den mha. denna metod
            self.viable = False
            self.model.grid.remove_agent(self);
            self.model.schedule.remove(self);

    #PROLIFERATION METHOD
    def proliferate(self):
         try:
            self.model.generate_agents(Tumor_cells, "proliferate", 1, self.position); #will be changed to proliferate
            #print("Tumor cell generated, id = ", self.unique_id);
         except Exception as e:
              #print(f"Error while generating Tumor cell from agent  {self.unique_id} {e}")
              pass

    def step(self):
        self.tumor_endo_interaction();
        if random.randint(0,100) < 100*self.proliferation_prob:
            self.proliferate();
        if random.randint(0,100) < 100*self.death_prob:
            self.apoptosis()
        #if adjacent or diagonal cell contain(fibroblast) do Increase  * death_prob?
        #if cell_M.._dist < critDistToM:do Proliferation in empty cell * prolifiration_prob;
        #if cell_endo_dist > critDistHypoxia:Induce Endothelial Proliferation;


    

    
# Imports all the required classes from the needed modules for creating the Mesa-model
                    # Add the type of cell as an additional instance variable
        # OBS: Lägg till flera relevanta instansvariabler!!
    # Exempel på resterande metoder som tumörcellen kommer att behöva 
    #def step():
    #def migration():
    #def proliferation():
    #def resistance_Macrohpage():