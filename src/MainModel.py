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
    '''
    # MainModel

    ABM Model simulating prostate tumor micro environment. 
    Contains methods for model initiation, agent-agent-interactivity, data collection, data plotting, and simulation progression(step()). 
    '''
    # GENERATE A UNIQUE ID (not random)
    def get_next_unique_id(self):   
        """
        Generate the next unique ID.

        This helper method for `MainModel.generate_agents()` generates and adds a new sequential 
        number to `MainModel.used_ids[]`.

        Returns:
            int: The next unique ID.
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
                        #print("TRY")
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
        """
        Adds an agent to the simulation.

        Parameters:
        agent_type (type): The type or class of the agent being added.
        agent (Agent): The agent instance to be added to the simulation.

        The method performs the following actions:
        - Checks if the agent's position is within the bounds of the grid.
        - If valid, adds the agent to `agent_storage` under the specified `agent_type`.
        - Adds the agent to the simulation schedule.
        - Places the agent on the grid at its specified position.

        If the agent's position is outside the grid bounds, the method takes no action.
        """
        x, y = agent.position
        if x < self.grid.width and y < self.grid.height:
            self.agent_storage[agent_type][agent.unique_id]= agent
            self.schedule.add(agent)  
            self.grid.place_agent(agent, agent.position)
        else:
            pass

    #GENERATE POSITION SORTED LIST OF AGENTS OF SPECFIC TYPE 
    def get_agent_type_list(self, agent_type):
        """
        Retrieves a set of agents of a specific type.

        Parameters:
        agent_type (type): The type or class of agents to retrieve.

        Returns:
        set: A set containing all agents of the specified type stored in `agent_storage`.
        """
        agent_type_list = set()
        for unique_id, agent in self.agent_storage[agent_type].items():
            agent_type_list.add(agent)
        return agent_type_list
    
    # INITIALIZE MODEL - initialize the agents put on the grid by the previous method
    def __init__(self, num_steps=None, *args, **kwargs):
        """
        Initializes the model with the specified parameters and sets up the simulation.

        Parameters:
        num_steps (int, optional): The number of steps to run the simulation. Defaults to None.
        *args: Additional positional arguments for the superclass.
        **kwargs: Additional keyword arguments for the superclass.

        The initialization performs the following tasks:
        - Sets a fixed random seed for reproducibility.
        - Configures the grid with a size of 150x150 and disables toroidal wrapping.
        - Sets up a random activation schedule for agents.
        - Initializes storage for various agent types, such as Endothelial, Tumor_cells, M1, M2, and Fibroblast.
        - Generates predefined agents of each type and stores them in respective lists.
        - Initializes variables for tracking nutrient levels, agent counts, and other data.
        - Configures a DataCollector to collect model-level and agent-level data during the simulation.
        """
        #SET RANDOM SEED
        random.seed(4)
        
        #MODEL RUNNING:
        self.num_steps = num_steps
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
        self.generate_agents(M1, "default", 100);
        self.m1_list = self.get_agent_type_list(M1)
        self.generate_agents(M2, "default", 800);
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
        
        self.datacollector = DataCollector(
            model_reporters={
                "Total Agents": lambda m: len(m.schedule.agents),
                "Endothelial cells": lambda m: len(m.endothelial_list),
                "Tumor_cells": lambda m: len(m.tumor_cell_list),
                "M1": lambda m: len(m.m1_list),
                "M2": lambda m: len(m.m2_list),
                "Fibroblast": lambda m: len(m.fibroblast_list),
                "Nutrient levels": lambda m: m.nutrition_cap
                },
            agent_reporters={
                "Position": lambda a: a.pos,
            }
        )  
        

    #DATACOLLCETION
    def data_collection(self, *args):
        """
        Collects and records agent count and rate data at each simulation step.

        Parameters:
        *args: A variable-length argument list. The first argument determines the action to take:
            - "record" to store current agent count and rate data.
            - "count" followed by a specific agent type to return the current count for that type.
            - "rate" followed by a specific agent type to return the current rate of change for that type.

        Data Collected:
        - Agent counts for total agents and individual types (Endothelial, Tumor, M1, M2, and Fibroblast).
        - Rate of change in agent counts between consecutive steps.
        - Nutrient concentration as a ratio of available nutrition to grid area.

        Returns:
        - If "count" is provided as the first argument, returns the current count of the specified agent type.
        - If "rate" is provided, returns the current rate of change for the specified agent type.
        - Otherwise, stores the data in the respective record dictionaries.
        """
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
    def plot_data_basic(self):
        """
        Plots the counts of various agent types and nutrient concentration over time.

        The method collects data on the counts of agents (Total, Endothelial, Tumor, M1, M2, and Fibroblast)
        at each simulation step, as well as the nutrient concentration, and plots them using Matplotlib.

        The following plots are generated:
        - Agent counts for each type (Endothelial, Tumor, M1, M2, Fibroblast) over time.
        - Nutrient concentration over time.

        The x-axis represents the simulation steps, and the y-axis represents the count of agents or nutrient concentration.
        """
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

    def plot_data_overlap(self):
        """
        Plots the counts of various agent types and nutrient concentration over time with multiple y-axes.

        This method creates a plot where the x-axis represents the simulation steps, and the y-axes represent 
        the counts of different agent types and nutrient concentration at each step. Multiple y-axes are used 
        to display data for each agent type and nutrient concentration without overlap.

        The following plots are generated:
        - Total agents count on the primary y-axis.
        - Individual agent types (Endothelial, Tumor, M1, M2, and Fibroblast) each on a separate y-axis.
        - Nutrient concentration on a separate y-axis.

        All data is plotted over the simulation steps, and the plot is displayed with appropriate labels and legends.
        """
        # agent data
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
                count = self.agent_count_record[step][type]
                plot.append(count)
        
        # nutrient data
        nutrient_conc_over_time = []
        for step in self.nutrition_conc_record:
            nutrient_conc_over_time.append(self.nutrition_conc_record[step])

        # Create the main plot
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot the total agents count (primary y-axis)
        ax1.plot(steps, time_plots[0], label="total agents", color="blue")
        ax1.set_xlabel("time")
        ax1.set_ylabel("Total agents", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")

        # Create secondary y-axes for each dataset
        ax2 = ax1.twinx()
        ax2.plot(steps, time_plots[1], label="endothelial", color="green")
        ax2.set_ylabel("Endothelial cells", color="green")
        ax2.tick_params(axis='y', labelcolor="green")

        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))  # Offset the axis to avoid overlap
        ax3.plot(steps, time_plots[2], label="tumor cells", color="red")
        ax3.set_ylabel("Tumor cells", color="red")
        ax3.tick_params(axis='y', labelcolor="red")

        ax4 = ax1.twinx()
        ax4.spines['right'].set_position(('outward', 120))  # Further offset for clarity
        ax4.plot(steps, time_plots[3], label="m1", color="orange")
        ax4.set_ylabel("Macrophage 1", color="orange")
        ax4.tick_params(axis='y', labelcolor="orange")

        ax5 = ax1.twinx()
        ax5.spines['right'].set_position(('outward', 180))  # Further offset for clarity
        ax5.plot(steps, time_plots[4], label="m2", color="purple")
        ax5.set_ylabel("Macrophage 2", color="purple")
        ax5.tick_params(axis='y', labelcolor="purple")

        ax6 = ax1.twinx()
        ax6.spines['right'].set_position(('outward', 240))  # Further offset for clarity
        ax6.plot(steps, time_plots[5], label="fibroblast cells", color="brown")
        ax6.set_ylabel("Fibroblast cells", color="brown")
        ax6.tick_params(axis='y', labelcolor="brown")

        ax5 = ax1.twinx()
        ax6.spines['right'].set_position(('outward', 300))  # Further offset for clarity
        ax6.plot(steps, nutrient_conc_over_time, label="substrate", color="pink")
        ax6.set_ylabel("Nutrient Concentration", color="pink")
        ax6.tick_params(axis='y', labelcolor="pink")

        # Plot nutrient concentration on the main plot
        ax1.plot(steps, nutrient_conc_over_time, label="nutrient cap", color="black", linestyle="--")
        
        # Combine all legends from each axis
        fig.legend(loc="upper right", bbox_to_anchor=(1.2, 1))
        
        # Show plot
        plt.tight_layout()
        plt.show()

    #UPDATE AGENT_STORAGE{}
    def update_agent_storage(self):
        """
        Updates the agent storage to ensure it only contains agents that are currently in the schedule.

        This method compares the agents in `agent_storage` with the agents in the `schedule`. If any agents in 
        `agent_storage` are no longer in the schedule, they are removed from the storage.

        The method performs the following tasks:
        - Creates a set of agents currently in the schedule.
        - Iterates through each agent type in `agent_storage`.
        - Identifies agents in `agent_storage` whose unique IDs are not present in the schedule.
        - Removes these agents from the storage.

        The update ensures that `agent_storage` remains synchronized with the `schedule`.
        """
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
        """
        Returns the current nutrition capacity of the model.

        This method provides access to the `nutrition_cap` attribute, which represents the total available 
        nutrition in the model.

        Returns:
        - The current nutrition capacity value.
        """
        return self.nutrition_cap
    
    #CREATE NUTRITION CAP
    def update_nutrition_cap(self, val):
        """
        Updates the nutrition capacity by adding a specified value.

        This method modifies the `nutrition_cap` attribute by adding the provided value to it. This can be used 
        to increase or decrease the available nutrition in the model.

        Parameters:
        val (int or float): The value to add to the current nutrition capacity.

        Returns:
        None
        """
        self.nutrition_cap += val
    
    #EAT NEW NUTRITION CAP
    def eat_nutrition(self, val):
        """
        Reduces the nutrition capacity by a specified value.

        This method decreases the `nutrition_cap` attribute by the provided value. This simulates the consumption 
        or depletion of available nutrition in the model.

        Parameters:
        val (int or float): The amount of nutrition to subtract from the current capacity.

        Returns:
        None
        """
        self.nutrition_cap -= val

    def print_step_data():
        """
        Prints the current data for the simulation step.

        This method outputs relevant information for the current step of the simulation, including:
        - The current `nutrition_cap` level.
        - The counts of agents stored in `agent_count_record` for the current step.
        - The rates of agent changes stored in `agent_rate_record` for the current step.
        - The current `nutrition_cap` value and its concentration relative to the grid's size.
        - A sample of the M1 agents (`m1_list`) for testing purposes.

        Returns:
        None
        """
        #PRINT STEP DATA:
        print(f'Current nutrition_cap levels: {self.nutrition_cap}')
        print(f'Counts:{self.agent_count_record[self.step_count]}')
        print(f'Rates:{self.agent_rate_record[self.step_count]}')
        print(f'Nutrition: {self.nutrition_cap}, Nutrition Concentration: {self.nutrition_cap/(self.grid.width*self.grid.height)}')
        print(f'Test sample : {self.m1_list}')
    # STEP METHOD 
    def step(self): 
        """
        Advances the simulation by one step.

        This method updates the simulation by performing the following tasks:
        - Ends the simulation if the number of steps exceeds `num_steps`.
        - Records data for the current step.
        - Collects model data using the `datacollector`.
        - Advances the simulation schedule by one step.
        - Updates the lists of agent types (Endothelial, Tumor cells, M1, M2, Fibroblasts).
        - Removes agents from `agent_storage` that are no longer in the schedule.
        - Increments the `step_count` for the next simulation step.

        If the simulation reaches the maximum number of steps (`num_steps`), it will stop and generate plots of the data.

        Returns:
        None
        """

        # END OF SIMULATION AND PRINT PLOTS
        if self.num_steps != None and self.step_count > self.num_steps:
            self.running = False
            print("Simulation reached the maximum number of steps")

            #COLLECTING STORED DATA
            model_df = self.datacollector.get_model_vars_dataframe()
            agent_df = self.datacollector.get_agent_vars_dataframe()

            #DOWNLOAD DATA FILES
            model_df.to_excel("model_data.xlsx", index=False)
            agent_df.to_excel("agent_data.xlsx", index=False)
            
            #PLOT DATA
            self.plot_data_overlap()
            self.plot_data_basic()

        self.data_collection("record")

        #MESA DATA COLLECTION
        self.datacollector.collect(self)

        #NEXT STEP
        self.schedule.step() 
    
        #GENERATE LIST OF ENDOTHELIAL CELLS
        self.endothelial_list = self.get_agent_type_list(Endothelial)
        self.tumor_cell_list = self.get_agent_type_list(Tumor_cells)
        self.m1_list = self.get_agent_type_list(M1)
        self.m2_list = self.get_agent_type_list(M2)
        self.fibroblast_list = self.get_agent_type_list(Fibroblast)
        
        #UPDATE self.agent_storage{} TO REMOVE AGENTS THAT DO NOT APPEAR IN self.scheduler
        self.update_agent_storage()
        
        #PRINT STEP DATA:
        #self.print_step_data()

        self.step_count += 1


#-------------------------------------------------#-------------------------------------------------
# Create a CanvasGrid for visualization
#In ModelSetver.py
