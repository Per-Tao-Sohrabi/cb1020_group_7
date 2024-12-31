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
    def __init__(self, unique_id, position, model, *args): #Position inputed as (x,y)
        super().__init__(unique_id, model);
        self.model = model;
        self.unique_id = unique_id;
        self.position = position;
        self.viable = True

        #SET RANDOM SEED
        random.seed(5)
        # All the relevant properties (instance variables) for the tumor cell are initiated 
        #DEFAULTS
        
        #BASICS
        self.proliferation_prob = 0.0846
        self.migration_prob = 0.1167 
        self.death_prob = 0.00284
        self.initial_resist_M1_prob = 0
        self.resistance_M1_prob = 0.004
        self.lifespan = 150 #steps
        
        #KINETIC PARAMETERS:
        self.qs_max = 1.5 #µmol oxygen
        self.Ks_substrate = 1000 #according to GPT oxygen
        self.mu_max = 0.06 #
        self.Ks_growth = 100/(self.model.grid.width*self.model.grid.width) #µmol/L
        
        #HYPOXIA PARAMETERS
        self.max_signal_dist = 20
        self.optimal_signal_dist = 12
        self.hypoxia_thresholds = [2.0, 13.0, 14.0];

        #ENDO TRACKINGs
        self.nearest_endo = None;
        self.nearest_dist = None;
        self.prev_dist = None;
        if len(args) > 0:
            mothers_nearest_dist = args[0]
            self.prev_dist = mothers_nearest_dist #previous distance set
            self.set_nearest_endo() #identify nearest endo during initialization
        elif len(args) == 0:
            self.set_nearest_endo('default')
        
        #INTERACTION PARAMETERS (Distance Depen dent) -> self.tumor_endo_interaction() (NOT STANDARDIZED RANGES)
        self.death_intensity = 1.7  #1.7
        self.prolif_inhib_intensity = 0.6 #0.04
        self.angiogenesis_intensity = 0.8 #0.8
        self.optimal_signal_dist_significane = 0 #0.01

        #AGE PARAMETERS
        self.recParam1 = 0

        #HUNGER PARAMETERS:
        self.prolif_inhibition = 0
        self.intensify_death = 0
        self.migration_inhibition = 0

        #print(self.prev_dist)
    
    #SETTERS
    def set_nearest_endo(self, *args):
        endothelial_agents = self.model.endothelial_list; #endothelial_list is a list containing class type objects as elements.
        #print(f'Endothelial List: {self.model.endothelial_list}')
        counter = 1
        nearest_endo = None                     # initiate variable
        nearest_dist = None                     # initiate variable
        #FIND NEAREST ENDO
        for agent in endothelial_agents:
            x_other, y_other = agent.position
            x_self, y_self, = self.position
            distance_i = ((y_other-y_self)**2 + (x_other-x_self)**2)**(1/2)
            #print("SET!")
            #print(counter)

            #print(f'The distance between tumor_cell {self.unique_id} and endo cell {agent.unique_id} is {distance_i}')
            if nearest_endo is None or distance_i < nearest_dist:
                nearest_endo = agent
                nearest_dist = distance_i
             #   print(f'nearest dist {nearest_dist}')
            
            counter += 1
        
        
        #print(f'Nearest distance between TC {self.unique_id} and endo {nearest_endo.unique_id} = {nearest_dist}')
        #update new endo and dist
        self.nearest_endo = nearest_endo
        self.nearest_dist = nearest_dist
        
        #RECORD CURR DIST
        if len(args) > 0 and args[0] == 'default':
            #print("HEJ HEJ")
            self.prev_dist = self.nearest_dist
        #    print(f'near dist={self.nearest_dist}, prev dist ={self.prev_dist}')

        #print(f'near dist={nearest_dist}, prev dist ={self.prev_dist}')

        return nearest_endo, nearest_dist
    
    def set_proliferation_prob(self, *args):
        if args[0] == 'default':
            self.proliferation_prob = 0.0846
        elif args[0] != 'default':
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
   
    def set_angiogenesis_intensity(self, *args):
        if len(args) == 1:
            self.angiogenesis_intensity = args[0]
    
    #TUMOR-ENDOTHELIAL CELL INTERACTIONS
    def tumor_endo_interaction(self):
        #print(f'Attempting tumor-endo interaction for agent: {self.unique_id}')

        #NOTATIONS
        best_dist = self.optimal_signal_dist
        curr_dist = self.nearest_dist
        threshold1 = self.hypoxia_thresholds[0]; threshold2 = self.hypoxia_thresholds[1]; threshold3 = self.hypoxia_thresholds[2]
        diff = self.prev_dist - self.nearest_dist #This only works if set_nearest_endo is initialized.
        print(f'Prev dist: {self.prev_dist}, Curr dist: {curr_dist}')
        if diff != 0:
            diff_sign = diff/abs(diff)
        else:
            diff_sign = 0

        #INTERACTION ATTIBUTE PARAMETERS *FOR LOGISTIC ZONE*
        #  Death Intensity
        death_intensity = self.death_intensity
        delta_death_factor = death_intensity  * abs(curr_dist-threshold3)/threshold3 #större
        death_factor = delta_death_factor
        
        #  Tumor Proliferation Inhibition
        inhib_intensity = self.prolif_inhib_intensity 
        if curr_dist != 0:
            prolif_inhibition_level =  inhib_intensity*diff_sign * (curr_dist - threshold2)/curr_dist #relevant in the logistic zone
        elif curr_dist == 0:
            prolif_inhibition_level =  0

        proliferation_factor = 1-prolif_inhibition_level    # Higher inhibition level > smaller factor > smaller proliferation.
        
        #  Induction Level
        induct_intensity = self.angiogenesis_intensity 
        speed_dampening = self.optimal_signal_dist_significane #Lowers the significance of the optimal signal distance.
        if best_dist == curr_dist:
            induction_factor = 1
        else:
            induction_factor = induct_intensity * 1 / (1 + abs(best_dist-speed_dampening*curr_dist)) #0.9 because the milden the drop in induction intensity when removed from best distance. 
        
        self.set_nearest_endo('default'); #updates prev distance and new distance.
        
        print(f'Diff Sign: {diff_sign}')
        print(f'Proliferation Inhibition Level: {prolif_inhibition_level}')
        print(f'Proliferation Factor : {proliferation_factor}')
        print(f'diff: {diff}')

        #========ZONES========
        #DISCRETE ZONE
        if self.nearest_dist <= threshold1: #withing Lower bound
            self.set_proliferation_prob(0.15, "value")   #+20%
        elif threshold1 < self.nearest_dist <= threshold2:
            self.set_proliferation_prob("default")     #default

        #LOGISTIC ZONE
        elif self.nearest_dist > threshold2:
            if diff != 0:
                self.set_proliferation_prob(proliferation_factor, "proportion")
                if self.nearest_dist > threshold3:
                    self.set_death_prob(death_factor, "proportion")
            self.nearest_endo.targeted_proliferation(self.position, induction_factor)          
        #print(f'TUMOR DATA id = {self.unique_id}')
        #print(f'* Tumor Age = {150-self.lifespan}')
        #print(f'* Proliferation Prob = {self.proliferation_prob}')
        #print(f'* Death Prob = {self.death_prob}')
        #print(f'* Direction sign {diff_sign}')
        #print(f'* Distance to nearest Endothelial cell = {self.nearest_dist}')
        


        #elif self.nearest_dist > self.hypoxia_thresholds[2]:
        #    self.set_death_prob(2, "proportion") 
    
    #MIGRATION
    def migrate(self):
        #IN SITU MIGRATION???
        if random.randint(0,100) < 100*self.migration_prob:
            #print("TUMOR CELL MIGRATED")
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
                pass #print(f"Does not have a position: {self.unique_id}")
            elif self.position != None:
                self.viable = False
                self.model.grid.remove_agent(self);
                self.model.schedule.remove(self);

    #PROLIFERATION METHOD
    def proliferate(self):
         self.model.generate_agents(Tumor_cells, "proliferate", 1, self.position, self.nearest_dist); #will be changed to proliferate
         '''
         try:
            self.model.generate_agents(Tumor_cells, "proliferate", 1, self.position, self.nearest_dist); #will be changed to proliferate
            #print("Tumor cell generated, id = ", self.unique_id);
         except Exception as e:
              print(f'Position: {self.position}')
              print(f"Error while generating Tumor cell from agent  {self.unique_id} {e}")
              pass
              '''
    #AGE
    def age(self):
        if self.lifespan > 0:

            self.lifespan -= 1
            self.recParam1 += 0.001

            chance_of_death = self.recParam1
            decreased_prolif = self.recParam1*1.3
            
            self.death_prob += chance_of_death
            self.proliferation_prob -= decreased_prolif
        
        elif self.lifespan == 0:
            self.set_death_prob(1, "value")

    #EAT
    def eat(self, val):
        self.model.eat_nutrition(val)

    #HUNGER (BROKEN)
    def hunger(self):
        #COUNT CELLS
        total_cells = self.model.grid.width*self.model.grid.height + self.model.data_collection("count", "total") 
        #COUNT NUTRITION
        nutrition_cap = self.model.nutrition_cap
        #COUNT RATIO # Smaller ratio >>> decreased pro parameters, increased de parameters.
        avg_consumption = int((10+3+5+1)/4)

        S = nutrition_cap/(self.model.grid.width*self.model.grid.height)       # nutrient_concentration
        
        nutrient_limit = 0.2
        
        if nutrition_cap <= 0:
            self.eat(0)
            self.set_angiogenesis_intensity(1.5)
            self.set_proliferation_prob(0, "value")
            print(nutrition_cap)

        elif nutrition_cap > 0:

            availability_ratio = total_cells/(nutrition_cap*avg_consumption)

            self.qs = (self.qs_max*S)/(self.Ks_substrate*S)
            print(f'Tumor cell qs: {self.qs}')                                                           # consumption rate

            self.eat(self.qs)                                                                                # eat substrate
            
            print(f'Nutrient concentration: {S}')
            if S >= nutrient_limit:                                          #
                new_prol_prob = (1 * S)/(S + self.Ks_growth)
                self.set_proliferation_prob(new_prol_prob, "value")

            if self.nearest_dist >self.hypoxia_thresholds[1]:
                print(f'ENDO-TUMOR Dist: {self.nearest_dist}')
                print(f'Hunger Adjusted Prolif Prob: {self.proliferation_prob}')
        #if depletion_ratio < 1:             #When nutrition is being depleted
        #    self.set_proliferation_prob(depletion_ratio, "proportion")
        #    #self.set_death_prob(1+depletion_ratio**1, "proportion")
        #    pass
        #if nutrition_cap <= 0:
        #    self.set_proliferation_prob(0, "value")
    
     
    #STEP 
    def step(self):
        #self.eat(10)
        #self.hunger()
        self.age()
        print(f'Life Span: {self.lifespan}')
        print(f'Age Adjusted Prolif Prob: {self.proliferation_prob}')
        self.migrate();
        self.tumor_endo_interaction();
        print(f'Confirm Prolif Prob: {self.proliferation_prob}')
        if random.randint(0,100) < 100*self.proliferation_prob:
            self.proliferate();
        if random.randint(0,100) < 100*self.death_prob:
            self.apoptosis()

        #if adjacent or diagonal cell contain(fibroblast) do Increase  * death_prob?
        #if cell_M.._dist < critDistToM:do Proliferation in empty cell * prolifiration_prob;
        #if cell_endo_dist > critDistHypoxia:Induce Endothelial Proliferation;