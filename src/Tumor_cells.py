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
        #DEFAULTS
        
        #basics
        self.proliferation_prob = 0.0846
        self.migration_prob = 0.1167
        self.death_prob = 0.00284
        self.initial_resist_M1_prob = 0
        self.resistance_M1_prob = 0.004

        #Hypoxia parameters
        self.max_signal_dist = 20
        self.optimal_signal_dist = 10
        self.hypoxia_thresholds = [3.0, 10.0, 22.0];

        #endo tracking
        self.nearest_endo = None;
        self.nearest_dist = None;
        self.prev_dist = None;

        self.set_nearest_endo() #identify nearest endo during initialization
    
    #SETTERS
    def set_nearest_endo(self):
        endothelial_agents = self.model.endothelial_list; #endothelial_list is a list containing class type objects as elements.
        counter = 1
        nearest_endo = None
        nearest_dist = None#
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
        #save old dist
        self.prev_dist = self.nearest_dist
        #update new endo and dist
        self.nearest_endo = nearest_endo
        self.nearest_dist = nearest_dist
        return nearest_endo, nearest_dist
    
    def set_proliferation_prob(self, *args):
        if args[0] == "default":
            self.proliferation_prob = 0.0846
        else:
            val = args[0]
            type = args[1]
            
            if type == "proportion":
                self.proliferation_prob = self.proliferation_prob * val
            if type == "value":
                self.proliferation_prob = val
            else:
                pass

    def set_death_prob(self, *args):
        if args[0] == "default":
            self.death_prob = 0.00284
        else:
            val = args[0]
            type = args[1]
            
            if type == "proportion":
                self.death_prob = self.death_prob * val
            if type == "value":
                self.death_prob = val
            else:
                pass
        pass
    
    def set_optimal_signal_dist(self, *args):
        self.optimal_signal_dist = args[0]

    def tumor_endo_interaction(self):
        self.set_nearest_endo(); #updates prev distance and new distance.
        
        #NOTATIONS
        best_dist = self.optimal_signal_dist
        curr_dist = self.nearest_dist
        threshold1 = self.hypoxia_thresholds[0] #Lower hypoxia limit
        threshold2 = self.hypoxia_thresholds[1] #Upper hypoxia limit
        threshold3 = self.hypoxia_thresholds[2]
        diff = self.prev_dist - self.nearest_dist #This only works if set_nearest_endo is initialized.
        diff_sign = 0
        
        if diff != 0:
            diff_sign = abs(diff)/diff

        #INTERACTION ATTIBUTES    
        delta_death_factor = (threshold3-curr_dist/threshold3)
        death_factor = 1-delta_death_factor

        prolif_deactivation_level =  diff_sign*(curr_dist - threshold2)/curr_dist #relevant in the logistic zone
        proliferation_factor = 1-prolif_deactivation_level

        induction_factor = 0 #Set seperatley 
        #Set induction factor
        if best_dist == curr_dist:
            induction_factor = 1
        else:
            induction_factor = 1 / (1 + abs(best_dist-curr_dist))

        #DISCRETE ZONE
        if self.nearest_dist <= self.hypoxia_thresholds[0]: #withing Lower bound
            self.set_proliferation_prob(0.15, "val")   #+20%
        elif self.hypoxia_thresholds[0] < self.nearest_dist <= self.hypoxia_thresholds[1]:
            self.set_proliferation_prob("default")     #default
        
        #LOGISTIC ZONE
        elif self.nearest_dist > self.hypoxia_thresholds[1]:
            if diff != 0:
                self.set_proliferation_prob(proliferation_factor, "proportion")
                self.set_death_prob(death_factor, "proportion")
            self.nearest_endo.targeted_proliferation(self.position, induction_factor)          
            #if diff > 0:
            #   self.set_proliferation_prob(delta_proliferation_prob, "proportion") #decrease proliferation rate by few percent
            #    self.set_death_prob(death_factor, "proportion")
            #elif diff < 0:
            #    self.set_proliferation_prob(1.01, "proportion") #increase slightly as endo gets closer
            #Induce proliferation in endothelial cell
            


        #elif self.nearest_dist > self.hypoxia_thresholds[2]:
        #    self.set_death_prob(2, "proportion")
    
    #MIGRATION
    def migrate(self):
        #IN SITU MIGRATION???
        if random.randint(0,100) < 100*self.migration_prob:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            
            # Filter only empty positions
            empty_positions = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos)]

            #Pick an empty position if there are any
            if len(empty_positions) > 0:
                new_position = self.random.choice(empty_positions)
                self.model.grid.move_agent(self, new_position)

        #MIGRATION ACROSS BLOOD VESSLE
        
    #APOPTOSIS METHOD:
    def apoptosis(self): # Försöka modellera om cellen är tillräckligt nära en anti-cancer-makrofag så dödas den mha. denna metod
            if self.position == None:
                print(f"Does not have a position: {self.unique_id}")
            elif self.position != None:
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
        print(f'Attempting tumor-endo interaction for agent: {self.unique_id}')
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