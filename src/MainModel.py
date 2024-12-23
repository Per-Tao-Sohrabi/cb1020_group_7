from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import random as random;
from Endothelial import Endothelial;
from Tumor_cells import Tumor_cells; 
from M1 import M1;
# from M2 import M2
# from Fibroblast import Fibroblast;



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
        for i in range(amount):
            unique_id = self.get_next_unique_id()
            if brush_stroke == "proliferate":
                agent_type = agent_type;
                # Handle tumor cell proliferation here without removing the original
                position = args[0];
                # Get all adjacent positions (Moore neighborhood, excluding center)
                adjacent_positions = self.grid.get_neighborhood(
                    pos=position, moore=True, include_center=False, radius=1
                )
                # Filter positions to only include empty cells
                empty_positions = [pos for pos in adjacent_positions if self.grid.is_cell_empty(pos)] 
                if empty_positions:
                    # Randomly select one of the valid empty positions
                    next_position = random.choice(empty_positions)
                    
                    # Generate new Tumor_cell instance and place it
                    agent = agent_type(unique_id, next_position, self)
                    #self.add_agent(agent_type, agent)
                    #self.schedule.add(agent)
                    #self.grid.place_agent(agent, next_position)
                    agent_cache[unique_id] = agent
                else:
                    print(f"No empty cells available for tumor cell {unique_id} at position {position}.")

            elif brush_stroke == "default":                  # Default settings for generating agents
                agent_type = agent_type
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
                    self.add_agent(agent_type, agent)
                    #agent_cache[unique_id] = agent;
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
                    if new_x < self.grid.width and new_y < self.grid.height: # Handles the edge case when cells get generated outside the grid
                        #self.add_agent(agent_type, agent)
                        #self.grid.place_agent(agent, (new_x, new_y))
                        continue
            self.add_agent(agent_type, agent)
        pass # allows the agents that exist in the cache to be saved in the model's agent storage 

    #ADD AGENT TO MODEL (This is a helper method for the above method)
    def add_agent(self, agent_type, agent):
        '''
        Helper method for MainModel.generate_agents()

        Adds an agent to (1) self.agent_storage, (2) self.schedule, and (3) self.grid.
        '''
        self.agent_storage[f"{agent_type}"][agent.unique_id]= agent
        self.schedule.add(agent)  
        self.grid.place_agent(agent, agent.position)



    # INITIALIZE MODEL - initialize the agents put on the grid by the previous method
    def __init__(self, *args, **kwargs):
        """
        Initialize the MainModel.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        #Model fields
        super().__init__(*args, **kwargs)
        self.grid = MultiGrid(150, 150, torus=False);
        self.schedule = SimultaneousActivation(self);
        self.agent_storage = {
            "<class 'Endothelial.Endothelial'>": {},
            "<class 'Tumor_cells.Tumor_cells'>": {},
            "<class 'M1.M1'>": {},
            # Add other agent types here if needed
        }
         #saves agent_chaces from self.generate_agents(*args);
        self.used_ids = set();
        #self.generate_agents(Tumor_cells,1);
        self.generate_agents(Endothelial,"horizontal blood vessle", 1000);
        self.generate_agents(Endothelial,"vertical blood vessle", 1000);
        self.generate_agents(Tumor_cells, "default", 1);
        self.generate_agents(M1, "default", 10);
        #self.generate_agents(M1, 10);
        #self.generate_agents(M2, 10);
        #self.generate_agents(Fibroblast, 5);
        self.step_data = {};
        
        for agent_type in self.agent_storage:      # Initialize "step_data" for each agent-type (cell-type)
            self.step_data[agent_type] = {}  

    # STEP METHOD 
    def step(self):  # OBS: preliminary code, have not tested it yet!
        """
        Advance the simulation by one step, updating the model and agents.
        """
        #UPDATE AGENT_TYPE STEP DATA
        now_step = self.schedule.steps
        for agent_type, agents in self.agent_storage.items():       #Checks out list of agents of specific class.
            self.step_data[agent_type][now_step] = {                #Checks each agent's position.
                "number": len(agents),
                "position": [agent.position for agent in agents]
            }

        # The step is taken 
        self.schedule.step()               

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
    portrayal = {}

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

    return portrayal

# Set up the visualization canvas
canvas_element = CanvasGrid(agent_portrayal, 150, 150, 1200, 1200) 

# Create the ModularServer to run the visualization
server = ModularServer(MainModel, [canvas_element], "Prostate Environment Simulation")
server.port = 8521  # You can set a custom port
# Run the visualization server
server.launch()
