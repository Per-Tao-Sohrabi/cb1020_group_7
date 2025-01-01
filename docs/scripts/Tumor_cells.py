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
    """
    Class representing tumor cells in the model.
    Tumor cells can be cancerous or non-cancerous. Cancerous cells can induce endothelial growth, 
    migrate, proliferate, and interact with endothelial cells.

    Attributes:
        unique_id: The unique identifier for the agent.
        position: The position of the agent in the model grid.
        model: The model in which the agent resides.
        viable: Indicates if the tumor cell is viable.
        proliferation_prob: Probability of tumor cell proliferation.
        migration_prob: Probability of tumor cell migration.
        death_prob: Probability of tumor cell death.
        lifespan: Lifespan of the tumor cell (in steps).
        qs_max: Maximum oxygen concentration.
        qs: Current oxygen concentration.
        Ks_substrate: Substrate concentration for growth.
        mu_max: Maximum growth rate.
        Ks_growth: Growth rate constant.
        hypoxia_thresholds: Thresholds for different levels of hypoxia.
        nearest_endo: The nearest endothelial cell.
        nearest_dist: The distance to the nearest endothelial cell.
        prev_dist: The previous distance to the nearest endothelial cell.
    """
    #Constructor
    def __init__(self, unique_id, position, model, *args): #Position inputed as (x,y)
        """
        Initialize a tumor cell with the given parameters.

        Args:
            unique_id: Unique identifier for the agent.
            position: The position of the agent on the grid as a tuple (x, y).
            model: The model to which the agent belongs.
            *args: Optional arguments, including the previous distance to the nearest endothelial cell.
        """
        super().__init__(unique_id, model);
        self.model = model;
        self.unique_id = unique_id;
        self.position = position;
        self.viable = True

        #SET RANDOM SEED
        random.seed(5)
        
        #BASICS
        self.proliferation_prob = 0.0846
        self.migration_prob = 0.1167 
        self.death_prob = 0.00284
        self.initial_resist_M1_prob = 0
        self.resistance_M1_prob = 0.004
        self.lifespan = 150 #steps
        
        #KINETIC PARAMETERS:
        self.qs_max = 30 #µmol oxygen
        self.qs = 0
        self.Ks_substrate = 5 #according to GPT oxygen
        self.mu_max = 0.06 #
        self.Ks_growth = 1000/(self.model.grid.width*self.model.grid.width) #µmol/L
        
        #HYPOXIA PARAMETERS
        self.max_signal_dist = 20
        self.optimal_signal_dist = 12
        self.hypoxia_thresholds = [2.0, 7.0, 25.0];

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
            
        self.diff = self.prev_dist - self.nearest_dist #This only works if set_nearest_endo is initialized.
        #print(f'Prev dist: {self.prev_dist}, Curr dist: {curr_dist}')
        if self.diff != 0:
            self.diff_sign = self.diff/abs(self.diff)
        else:
            self.diff_sign = 0
        
        #INTERACTION PARAMETERS (Distance Depen dent) -> self.tumor_endo_interaction() (NOT STANDARDIZED RANGES)
        self.death_intensity = 1.7  #1.7
        self.prolif_inhib_intensity = 0.4#0.04
        self.angiogenesis_intensity = 0.08 #0.8 #Keep it smaller for beutiful branching
        self.optimal_signal_dist_significane = 0.0 #0.01

        #AGE PARAMETERS
        self.recParam1 = 0

        #HUNGER PARAMETERS:
        self.prolif_inhibition = 0
        self.intensify_death = 0
        self.migration_inhibition = 0

        #print(self.prev_dist)
    
    #SETTERS
    def set_nearest_endo(self, *args):
        """
        Set the nearest endothelial cell to the tumor cell.

        Args:
            *args: Optional argument for default behavior.
        
        Returns:
            nearest_endo: The nearest endothelial agent.
            nearest_dist: The distance to the nearest endothelial agent.
        """
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

            if nearest_endo is None or distance_i < nearest_dist:
                nearest_endo = agent
                nearest_dist = distance_i
             #   print(f'nearest dist {nearest_dist}')
            
            counter += 1
        
        #update new endo and dist
        self.nearest_endo = nearest_endo
        self.nearest_dist = nearest_dist
        
        #RECORD CURR DIST
        if len(args) > 0 and args[0] == 'default':
            #print("HEJ HEJ")
            self.prev_dist = self.nearest_dist

        return nearest_endo, nearest_dist
    
    def set_proliferation_prob(self, *args):
        """
        Set the proliferation probability for the tumor cell.

        Args:
            *args: Can specify a value and type (proportion or value).
        """
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
        """
        Set the death probability for the tumor cell.

        Args:
            *args: Can specify a value and type (proportion or value).
        """
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
        """
        Set the optimal signaling distance for angiogenesis.

        Args:
            *args: A single argument specifying the optimal distance.
        """
        self.optimal_signal_dist = args[0]
   
    def set_angiogenesis_intensity(self, *args):
        """
        Set the intensity of angiogenesis (blood vessel growth).

        Args:
            *args: A single argument specifying the intensity.
        """
        if len(args) == 1:
            self.angiogenesis_intensity = args[0]
    
    def print_agent_data(self):
        """
        Print relevant data for the tumor cell.

        Includes information about the tumor's age, proliferation probability,
        death probability, direction sign, and distance to the nearest endothelial cell.
        """
        print(f'TUMOR DATA id = {self.unique_id}')
        print(f'* Tumor Age = {150-self.lifespan}')
        print(f'* Proliferation Prob = {self.proliferation_prob}')
        print(f'* Death Prob = {self.death_prob}')
        print(f'* Direction sign {self.diff_sign}')
        print(f'* Distance to nearest Endothelial cell = {self.nearest_dist}')

    #TUMOR-ENDOTHELIAL CELL INTERACTIONS
    def tumor_endo_interaction(self):
        """
        Perform interaction between the tumor cell and the nearest endothelial cell.

        This includes modifying the proliferation probability, death probability,
        and angiogenesis intensity based on the distance to the endothelial cell.
        """
        #print(f'Attempting tumor-endo interaction for agent: {self.unique_id}')
        #NOTATIONS
        best_dist = self.optimal_signal_dist
        curr_dist = self.nearest_dist
        threshold1 = self.hypoxia_thresholds[0]; threshold2 = self.hypoxia_thresholds[1]; threshold3 = self.hypoxia_thresholds[2]
        diff = self.diff
        diff_sign = self.diff_sign

        #INTERACTION ATTIBUTE PARAMETERS *FOR LOGISTIC ZONE*
        #  Death Intensity
        death_intensity = self.death_intensity
        delta_death_factor = death_intensity  * abs(curr_dist-threshold3)/threshold3 
        death_factor = delta_death_factor
        
        #  Tumor Proliferation Inhibition
        inhib_intensity = self.prolif_inhib_intensity 
        if curr_dist != 0:
            prolif_inhibition_level =  inhib_intensity*diff_sign * (curr_dist - threshold2)/curr_dist #relevant in the logistic zone
        elif curr_dist == 0:
            prolif_inhibition_level =  0

        proliferation_factor = 1-prolif_inhibition_level  # Higher inhibition level -> smaller factor -> smaller proliferation.
        
        #  Induction Level
        induct_intensity = self.angiogenesis_intensity 
        speed_dampening = self.optimal_signal_dist_significane #Lowers the significance of the optimal signal distance.
        if best_dist == curr_dist:
            induction_factor = 1
        else:
            induction_factor = induct_intensity * 1 / (1 + abs(best_dist-speed_dampening*curr_dist)) 
        
        self.set_nearest_endo('default'); #updates prev distance and new distance.
        
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

        #PRINT AGENT DATA:
        #self.print_agent_data()
    
    #MIGRATION
    def migrate(self):
        """
        Move the tumor cell to a neighboring empty cell with a probability 
        defined by the migration probability.
        """
        #IN SITU MIGRATION???
        if random.randint(0,100) < 100*self.migration_prob:
            #print("TUMOR CELL MIGRATED")
            if self.pos != None:
                possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
                
                # Filter only empty positions
                empty_positions = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos)]

                #Pick an empty position if there are any
                if len(empty_positions) > 0:
                    new_position = self.random.choice(empty_positions)
                    self.model.grid.move_agent(self, new_position)

        #MIGRATION ACROSS BLOOD VESSLE
        #To be Continued        
    
    #APOPTOSIS METHOD:
    def apoptosis(self): 
        """
        Induce apoptosis (programmed cell death) for the tumor cell if it is 
        sufficiently close to an anti-cancer macrophage or if certain conditions are met.
        """
        if self.position == None:
            pass 
        elif self.pos != None and self.position != None:
            #print("DEAAD!")
            self.viable = False
            if self.position != None:
                self.model.grid.remove_agent(self);
                self.model.schedule.remove(self);

    #PROLIFERATION METHOD
    def proliferate(self):
        """
        Generate new tumor cells by proliferation.

        A new tumor cell is created at the same position as the current cell.
        """
        try:
            self.model.generate_agents(Tumor_cells, "proliferate", 1, self.position, self.nearest_dist); 
        except Exception as e:
            print(f'Position: {self.position}')
            print(f"Error while generating Tumor cell from agent  {self.unique_id} {e}")
            pass
            
    #AGE
    def age(self):
        """
        Age the tumor cell, reducing its lifespan and modifying the proliferation 
        and death probabilities based on age.
        """
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
    def eat(self, *args):
        """
        Simulate the tumor cell eating nutrition based on the available concentration.

        Args:
            *args: Can specify a custom nutrient value.
        """

        S = self.model.nutrition_cap/(self.model.grid.width*self.model.grid.height) # nutrient_concentration
        if S > 0:
            self.qs = (self.qs_max)*(S)/(self.Ks_substrate*S)
            self.model.eat_nutrition(self.qs)
        if len(args) > 0 :
            val = args[0]
            self.model.eat_nutrition(val)

    #HUNGER (BROKEN)
    def hunger(self):
        """
        Simulates the tumor cell's response to available nutrition.

        The method adjusts various parameters based on the nutrient concentration (S) 
        and the available nutrition cap in the model. It determines how hunger (low nutrition)
        influences proliferation, death probability, and other characteristics of the tumor cell.
        """
        #COUNT CELLS
        total_cells = self.model.grid.width*self.model.grid.height + self.model.data_collection("count", "total") 
        #COUNT NUTRITION
        nutrition_cap = self.model.nutrition_cap
        #COUNT RATIO # Smaller ratio >>> decreased pro parameters, increased de parameters.
        S = nutrition_cap/(self.model.grid.width*self.model.grid.height) # nutrient_concentration
        nutrient_limit = 2
        
        if nutrition_cap > nutrient_limit:
            self.eat()
            if nutrition_cap >= nutrient_limit: # consumption rate, eat substrate
                if S >= nutrient_limit and self.nearest_dist > self.hypoxia_thresholds[1] and self.qs < self.qs_max:
                    new_prol_prob = (1 * S)/(S + self.Ks_growth)
                    self.set_proliferation_prob(new_prol_prob, "proportion")
        elif nutrition_cap < nutrient_limit:
            self.eat(0)
            self.set_angiogenesis_intensity(1.5)
            self.set_death_prob(1.2, 'proportion')
            self.set_proliferation_prob(0, "proportion")
            #print(nutrition_cap)

    #STEP 
    def step(self):
        """
        Perform one step in the agent-based model.
        This involves moving, aging, proliferating, interacting with endothelial cells, and dying.
        """
        #print(f'TUMOR id: {self.unique_id}')
        #print(f'Initial proliferation_prob: {self.proliferation_prob}')
        #self.eat(10)
        self.hunger()
        #print(f'Hunger adjusted prolif prob: {self.proliferation_prob}')
        self.age()
        #print(f'Life Span: {self.lifespan}')
        #print(f'Age Adjusted Prolif Prob: {self.proliferation_prob}')
        self.migrate();
        self.tumor_endo_interaction();
        #print(f'Nearest distance: {self.nearest_dist}')
        #print(f'Distance adjusted Prolif prob: {self.proliferation_prob}')
        #print(f'Confirm Prolif Prob: {self.proliferation_prob}')
        #print(f'Death prob: {self.death_prob}')
        if random.randint(0,100) < 100*self.proliferation_prob:
            self.proliferate();
        if random.randint(0,100) < 100*self.death_prob:
            self.apoptosis()
