from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random;
from Endothelial import Endothelial;
from Tumor_cells import Tumor_cells; 
from M1 import M1;
from M2 import M2;
from Fibroblast import Fibroblast;



class MainModel(Model):
    """
    MainModel represents the prostate cancer simulation environment.
    """
    # GENERATE A UNIQUE ID (not random)
    def get_next_unique_id(self):   
        """
        Generate a unique ID for agents.

        Returns:
            int: A unique ID that has not been used before.
        """            
        unique_id = len(self.used_ids)          # Start with a base unique_id
        while unique_id in self.used_ids:       # Ensure the unique_id hasn't been used already
            unique_id += 1
        # Add the new ID to the used_ids set
        self.used_ids.add(unique_id)
        return unique_id
    
    #GENERATE AGENTS 
    def generate_agents(self, agent_type, brush_stroke, amount, *args):
        """
        Generate and place agents on the grid based on specified patterns.

        Args:
            agent_type (class): The type of agent to generate.
            brush_stroke (str): The pattern in which to place agents.
            amount (int): The number of agents to generate.
            *args: Additional arguments for specific patterns.

        Returns:
            dict: A cache of generated agents indexed by their unique IDs.
        """
        agent_cache = {};
        agent = None
        for i in range(amount):
            unique_id = self.get_next_unique_id()
            if brush_stroke == "proliferate":
                # Handle tumor cell proliferation here without removing the original
                mother_position = args[0];
                # Get all adjacent positions (Moore neighborhood, excluding center)
                adjacent_positions = self.grid.get_neighborhood(
                    pos=mother_position, moore=True, include_center=False, radius=1
                )
                # Filter positions to only include empty cells
                empty_positions = [pos for pos in adjacent_positions if self.grid.is_cell_empty(pos)] 
                if empty_positions:
                    # Randomly select one of the valid empty positions
                    daughter_position = random.choice(empty_positions)
                    
                    # Generate new Tumor_cell instance and place it
                    if agent_type == Tumor_cells:
                        mothers_nearest_dist = args[1]
                        print("TRY")
                        agent = agent_type(unique_id, daughter_position, self, mothers_nearest_dist)
                    else:
                        agent = agent_type(unique_id, daughter_position, self)
                    #self.add_agent(agent_type, agent)
                    #self.schedule.add(agent)
                    #self.grid.place_agent(agent, next_position)
                    agent_cache[unique_id] = agent
                else:
                    #print(f"No empty cells available for tumor cell {unique_id} at position {position}.")
                    pass
            elif brush_stroke == "default":                  # Default settings for generating agents
                x = self.random.randrange(self.grid.width)   # Declare Agent Coordinates
                y = self.random.randrange(self.grid.height)
                agent = agent_type(unique_id, (x,y), self)
                #self.add_agent(agent_type, agent)   # Declare new instance of agent according to mesa Agent initation.
                #self.schedule.add(agent);                    
                #self.grid.place_agent(agent, (x, y))         # Add the agents to the grid
                agent_cache[unique_id] = agent        
            elif brush_stroke == "horizontal blood vessle" or brush_stroke == "vertical blood vessle": # For other agents
                if i == 0:
                    x = 0;
                    y = random.randrange(self.grid.height);
                    agent = Endothelial(unique_id, (x,y), self); #uses i as id
                    agent_cache[unique_id] = agent;
                    #self.schedule.add(agent);  
                    #self.grid.place_agent(agent, (x, y));
                else:
                    prev_agent = agent_cache[unique_id-1]; #should not cause an indexing inconsistency if the blood vessle is generated in one instance. 
                    prev_x, prev_y = prev_agent.position;
                    if brush_stroke == "horizontal blood vessle":
                        x_inc = random.randint(0,1)
                        y_inc = random.randint(-1,1)
                    else:
                        x_inc = random.randint(-1,1)
                        y_inc = random.randint(0,1)
                    new_x, new_y = prev_x+x_inc, prev_y+y_inc
                    agent = Endothelial(unique_id, (new_x, new_y), self)
                    agent_cache[unique_id] = agent
                    #self.schedule.add(agent)
                     # Handles the edge case when cells get generated outside the grid
                        #self.add_agent(agent_type, agent)
                        #self.grid.place_agent(agent, (new_x, new_y))
            elif brush_stroke == "directed proliferation":

                #print("IN CONSTRUCTION")
                mother_position = args[0]
                #mother_target_coord = args[1]
                #GENERATE NEXT POSITION
                #1. Check Surroundings: get list of empty surrounding
                # Get all adjacent positions (Moore neighborhood, excluding center)
                #print(mother_position)
                x, y = mother_position                              #Edge case handeling where position is out of bounds
                if x < 0 or x >= self.grid.width or y < 0 or y >= self.grid.height:
                    return 

                adjacent_positions = self.grid.get_neighborhood(pos=mother_position, moore=True, include_center=False, radius=1)
                # Filter positions to only include empty cells
                empty_positions = [pos for pos in adjacent_positions if self.grid.is_cell_empty(pos)] 
                
                #2. Pick box in direction of target coord
                if empty_positions:
                    # Randomly select one of the valid empty positions
                    daughter_position = random.choice(empty_positions)
                    
                    # Generate new Tumor_cell instance and place it
                    agent = agent_type(unique_id, daughter_position, self)
                    #self.add_agent(agent_type, agent)
                    #self.schedule.add(agent)
                    #self.grid.place_agent(agent, next_position)
                    agent_cache[unique_id] = agent
                    #if mother.target
                else:
                    break
            if agent != None:
                self.add_agent(agent_type, agent)
        pass # allows the agents that exist in the cache to be saved in the model's agent storage 

    #ADD AGENT TO MODEL (This is a helper method for the above method)
    def add_agent(self, agent_type, agent):
        '''
        Helper method for MainModel.generate_agents()

        Adds an agent to (1) self.agent_storage, (2) self.schedule, and (3) self.grid.
        '''
        x, y = agent.position
        if x < self.grid.width and y < self.grid.height:
            self.agent_storage[agent_type][agent.unique_id]= agent
            self.schedule.add(agent)  
            self.grid.place_agent(agent, agent.position)
        else:
            pass

    #GENERATE POSITION SORTED LIST OF AGENTS OF SPECFIC TYPE 
    def get_agent_type_list(self, agent_type):
        agent_type_list = set()
        for unique_id, agent in self.agent_storage[agent_type].items():
            agent_type_list.add(agent)
        return agent_type_list
    
    # INITIALIZE MODEL - initialize the agents put on the grid by the previous method
    def __init__(self, *args, **kwargs):
        """
        Initialize the MainModel.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        #SET RANDOM SEED
        random.seed(4)
        
        #MODEL RUNNING:
        self.num_steps = 150

        #Model fields
        super().__init__(*args, **kwargs)
        self.grid = MultiGrid(150, 150, torus=False);
        self.schedule = RandomActivation(self);
        self.agent_storage = {
            Endothelial: {},
            Tumor_cells: {},
            M1: {},
            M2: {},
            Fibroblast: {}
            # Add other agent types here if needed
        }
         #saves agent_chaces from self.generate_agents(*args);
        self.used_ids = set();
        self.nutrition_cap = 0
        #Initiate nutrition_cap
        #self.generate_agents(Tumor_cells,1);
        self.generate_agents(Endothelial,"horizontal blood vessle", 1000);
        self.generate_agents(Endothelial,"vertical blood vessle", 1000);
        self.endothelial_list = self.get_agent_type_list(Endothelial)
        #self.nutrition_cap = self.grid.width*self.grid.height #len(self.endothelial_list)*1000                #GODTYCKLIKGT STARTVÄRDE 
        self.generate_agents(Tumor_cells, "default", 1);
        self.tumor_cell_list = self.get_agent_type_list(Tumor_cells)
        self.generate_agents(M1, "default", 50);
        self.m1_list = self.get_agent_type_list(M1)
        self.generate_agents(M2, "default", 200);
        self.m2_list = self.get_agent_type_list(M2)
        self.generate_agents(Fibroblast, "default", 10);
        self.fibroblast_list = self.get_agent_type_list(Fibroblast);
   
        #DATACOLLECTION
        self.step_count = 0
        self.agent_count_record = {}
        self.agent_rate_record = {}
        self.nutrition_conc_record = {}
        #self.avg_agent_specific_rates = {}

        # Initialize DataCollector
        '''
        self.datacollector = DataCollector(
            model_reporters={
                "Total Agents": lambda m: len(m.schedule.agents)
                "Endothelial cells": lambda m: len(m.endothelial_list)
                "Tumor_cells": lambda m: len(m.tumor_cells_list)
                "M1": lambda m: len(m.m1_list)
                "M2": lambda m: len(m.m2_list)
                "Fibroblast": lambda m: len(m.fibroblast_list)
                },
            agent_reporters={
                "Position": lambda a: a.pos,
            }
        )  
        '''

    #DATACOLLCETION
    def data_collection(self, *args):
        #CURRENT COUNTS
        agent_count = {
            "TOTAL":(len(self.endothelial_list) + len(self.tumor_cell_list) + len(self.m1_list) + len(self.m2_list) + len(self.fibroblast_list)),
            "ENDOTHELIAL":len(self.endothelial_list),
            "TUMOR":len(self.tumor_cell_list),
            "M1":len(self.m1_list),
            "M2":len(self.m2_list),
            "FIBROBLAST":len(self.fibroblast_list),
            }

        #DATA ANALYSIS
        if self.step_count > 0:
            dtotdt = agent_count["TOTAL"] - self.agent_count_record[self.step_count-1]["TOTAL"]
            dendothelialdt = agent_count["ENDOTHELIAL"] - self.agent_count_record[self.step_count-1]["ENDOTHELIAL"]
            dtumordt = agent_count["TUMOR"] - self.agent_count_record[self.step_count-1]["TUMOR"]
            dm1dt = agent_count["M1"] - self.agent_count_record[self.step_count-1]["M1"]
            dm2dt = agent_count["M2"] - self.agent_count_record[self.step_count-1]["M2"]
            dfibroblastdt = agent_count["FIBROBLAST"] - self.agent_count_record[self.step_count-1]["FIBROBLAST"]
        elif self.step_count == 0:
            dtotdt = 0
            dendothelialdt = 0
            dtumordt = 0
            dm1dt = 0
            dm2dt = 0
            dfibroblastdt = 0

        
        #CURRENT RATES
        agent_rate = {
            "TOTAl":dtotdt,
            "ENDOTHELIAL":dendothelialdt,
            "TUMOR":dtumordt,
            "M1":dm1dt,
            "M2":dm2dt,
            "FIBRObLAST":dfibroblastdt
        }

        #RECORD STEP DATA
        if args[0] == "record":
            self.agent_count_record[self.step_count] = agent_count
            self.agent_rate_record[self.step_count] = agent_rate
            self.nutrition_conc_record[self.step_count] = self.nutrition_cap/(self.grid.width*self.grid.height)
        
        if args[0] == "count":
            if args[1] == "total":
                return agent_count["TOTAL"]
            if args[1] == "endothelial":
                return agent_count["ENDOTHELIAL"]
            if args[1] == "tumor cells":
                return agent_count["TUMOR"]
            if args[1] == "m1":
                return agent_count["M1"]
            if args[1] == "m2":
                return agent_count["M2"]
            if args[1] == "fibroblast":
                return agent_count["FIBROBLAST"]
        
        if args[0] == "rate":
            if args[1] == "total":
                return agent_rate["TOTAl"]
            if args[1] == "endothelial":
                return agent_rate["ENDOTHELIAL"]
            if args[1] == "tumor cells":
                return agent_rate["TUMOR"]
            if args[1] == "m1":
                return agent_rate["M1"]
            if args[1] == "m2":
                return agent_rate["M2"]
            if args[1] == "fibroblast":
                return agent_rate["FIBROBLAST"]

    #PRINT DATA
    def plot_data(self):
            #agent data
            total_agents_count_over_time = []
            endothelial_agents_count_over_time = []
            tumor_agents_count_over_time = []
            m1_agents_count_over_time = []
            m2_agents_count_over_time = []
            fibroblast_ageents_count_over_time = []
            steps = np.linspace(0, self.step_count, self.step_count)
            
            keys = ["TOTAL", "ENDOTHELIAL", "TUMOR", "M1", "M2", "FIBROBLAST"]
            time_plots = [total_agents_count_over_time, endothelial_agents_count_over_time, tumor_agents_count_over_time, m1_agents_count_over_time, m2_agents_count_over_time, fibroblast_ageents_count_over_time]
            
            for type, plot in zip(keys, time_plots):
                for step in self.agent_count_record:
                    #print(step)
                    count = self.agent_count_record[step][type]
                    #print(count)
                    plot.append(count)
            
            #nutrient data
            nutrient_conc_over_time = []
            for step in self.nutrition_conc_record:
                nutrient_conc_over_time.append(self.nutrition_conc_record[step])

                #self.plot_graph(steps, plot, f'{type} over time"', "time", "agents")
            #plt.plot(steps, time_plots[1], label = "endothelial")
            plt.plot(steps, time_plots[2], label = "tumor cells")
            plt.plot(steps, time_plots[3], label = "m1")
            plt.plot(steps, time_plots[3], label = "m2")
            plt.plot(steps, time_plots[3], label = "fibroblast cells")
            plt.plot(steps, nutrient_conc_over_time, label = "nutrient cap")
            plt.legend()
            plt.show()
        
        #Lables
        #if title != None:
        #    plt.title(title)
        #if xLabel != None:
        #    plt.xlabel(xLabel)
        #if yLabel != None:
        #    plt.ylabel(yLabel)
        #plt.show()

    #UPDATE AGENT_STORAGE{}
    def update_agent_storage(self):
        schedule_agents_set = set(self.schedule.agents)
        
        # ITERATE THROUGH agent_storage{}
        for agent_type, agents_dict in self.agent_storage.items():  # agents_dict contains {unique_id: agent}
            
            # Collect unique IDs of agents to remove
            agents_to_remove = [
                unique_id for unique_id, agent in agents_dict.items()
                if agent not in schedule_agents_set
            ]
            
            # Remove agents that are not in the schedule
            for unique_id in agents_to_remove:
                del agents_dict[unique_id]
    
    #GET NUTRITION CAP
    def get_nutrition_cap(self):
        return self.nutrition_cap
    
    #CREATE NUTRITION CAP
    def update_nutrition_cap(self, val):
        self.nutrition_cap += val
    
    #EAT NEW NUTRITION CAP
    def eat_nutrition(self, val):
        self.nutrition_cap -= val

    # STEP METHOD 
    def step(self):  # OBS: preliminary code, have not tested it yet!
        """
        Advance the simulation by one step, updating the model and agents.
        """
        # END OF SIMULATION AND PRINT PLOTS
        if self.step_count > self.num_steps:
            self.running = False
            print("Simulation reached the maximum number of steps")
            
            #PLOT DATA
            self.plot_data()

            #total_agents_count_over_time = []
            #steps = np.linspace(0, self.step_count, self.step_count)
            #for step in self.agent_count_record:
            #    print(step)
            #    total_agents_count = self.agent_count_record[step]["TOTAL"]
            #    print(total_agents_count)
            #    total_agents_count_over_time.append(total_agents_count)
            
            #for plot in time_plots:
            #    self.plot_graph(steps, plot, f'{type} over time"', "time", "agents")
            #    return
        
        #DATA COLLECTION
        self.data_collection("record")

        #NEXT STEP
        self.schedule.step() 
    
        #GENERATE LIST OF ENDOTHELIAL CELLS
        self.endothelial_list = self.get_agent_type_list(Endothelial)
        self.tumor_cell_list = self.get_agent_type_list(Tumor_cells)
        self.m1_list = self.get_agent_type_list(M1)
        self.m2_list = self.get_agent_type_list(M2)
        self.fibroblast_list = self.get_agent_type_list(Fibroblast)
        
        #UPDATE NUTRITION CAP
        #self.eat_nutrition(self.grid.width*self.grid.height*0.01)            #simulate tissue maintainance consumption
        #self.update_nutrition_cap()

        #PRINT STEP DATA:
        print(f'Current nutrition_cap levels: {self.nutrition_cap}')
        #print(f'Number of Endothelial cells: {len(self.endothelial_list)}')
        #print(f'Number of Tumor cells: {len(self.tumor_cell_list)}')
        #print(f'Number of M1 cells: {len(self.m1_list)}')
        #print(f'Number of M2 cells: {len(self.m2_list)}')
        #print(f'Number of Fibroblast cells: {len(self.fibroblast_list)}')
        print(f'MODEL LEVEL DATA:')
        print(f'Counts:{self.agent_count_record[self.step_count]}')
        print(f'Rates:{self.agent_rate_record[self.step_count]}')
        print(f'Nutrition: {self.nutrition_cap}, Nutrition Concentration: {self.nutrition_cap/(self.grid.width*self.grid.height)}')
        #print(f'Test sample : {self.m1_list}')

        #UPDATE self.agent_storage{} TO REMOVE AGENTS THAT DO NOT APPEAR IN self.scheduler
        self.update_agent_storage()
        
        self.step_count += 1

        #Update self.agent_storage()
        #self.update_agent_storage()

#-------------------------------------------------#-------------------------------------------------
# Create a CanvasGrid for visualization
"""
    Define how agents are portrayed in the visualization.

    Args:
        agent (Agent): The agent to portray.

    Returns:
        dict: A portrayal dictionary specifying agent appearance.
"""
def agent_portrayal(agent):
    portrayal = {
        "Filled": "true",   # Ensure the shape is filled
    }

    if isinstance(agent, Tumor_cells):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0

        # Add a label if multiple agents are in the same cell for clarity
        cell_contents = agent.model.grid.get_cell_list_contents(agent.position)
        if len(cell_contents) > 1:
            portrayal["text"] = f"{len(cell_contents)}"
            portrayal["text_color"] = "white"

    elif isinstance(agent, Endothelial):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0

    elif isinstance(agent, M1):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0

    elif isinstance(agent, M2):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
    
    elif isinstance(agent, Fibroblast):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0


    return portrayal

# Set up the visualization canvas
canvas_element = CanvasGrid(agent_portrayal, 150, 150, 1200, 1200) 

# Create the ModularServer to run the visualization
server = ModularServer(
    MainModel, 
    [canvas_element], 
    "Prostate Environment Simulation",
    model_params={"num_steps": 500}
)

server.port = 8521  # You can set a custom port
# Run the visualization server
server.launch()
