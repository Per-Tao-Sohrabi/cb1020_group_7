from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

import random as random;
#from Tumor_cells import Tumor_cells; 
#from M1 import M1;
#from M2 import M2;
from Endothelial import Endothelial;
#from Fibroblast import Fibroblast;

class MainModel(Model):
    #GENERATE AGENTS 
    """
    # generate_methods(self, <class type>agent_type, <String>brush_Stroke, <aint>amount)
    ### Description
    This method belongs to MainModel.MainModel() which allows for specified generation patterns of mesa agents containing a self.position parmeter. 
    """
    def generate_agents(self, agent_type, brush_stroke, amount):
          agent_cache = {};
          for i in range(amount):
            if brush_stroke == "default": #default
                agent_type = agent_type;
                agent = agent_type(i, (x,y), self) #declare new instance of agent according to mesa Agent initation.
                self.schedule.add(agent);
                #Declare Agent Coordinates:
                x = self.random.randrange(self.grid.width);
                y = self.random.randrange(self.grid.height);
                self.grid.place_agent(agent, (x, y));
                i+=1
                #add the agents to the grid.
            elif brush_stroke == "horizontal blood vessle" or brush_stroke == "vertical blood vessle": #For other agents
                if i == 0:
                    x = 0;
                    y = random.randrange(self.grid.height);
                    agent = Endothelial(i, (x,y), self);
                    agent_cache[i] = agent;
                    self.schedule.add(agent);  
                    self.grid.place_agent(agent, (x, y));
                else:
                    prev_agent = agent_cache[i-1];
                    prev_x, prev_y = prev_agent.position;
                    if brush_stroke == "horizontal blood vessle":
                        x_inc = random.randint(0,1)
                        y_inc = random.randint(-1,1)
                    else:
                        x_inc = random.randint(-1,1)
                        y_inc = random.randint(0,1)
                    new_x, new_y = prev_x+x_inc, prev_y+y_inc;
                    agent = Endothelial(i, (new_x, new_y), self)
                    agent_cache[i] = agent;
                    self.schedule.add(agent);
                    if new_x < self.grid.width and new_y < self.grid.height: #Handles the edge case when cells get generated outside the grid.
                        self.grid.place_agent(agent, (new_x, new_y));


                
            
    #INSTANCE MODEL FIELDS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = MultiGrid(125, 135, torus=True);
        self.schedule = SimultaneousActivation(self);
        #self.generate_agents(Tumor_cells,1);
        self.generate_agents(Endothelial,"horizontal blood vessle", 1000);
        self.generate_agents(Endothelial,"vertical blood vessle", 1000);
        #self.generate_agents(M1, 10);
        #self.generate_agents(M2, 10);
        #self.generate_agents(Fibroblast, 5);
    
        '''
        self.cell_list = [];
        self.macrophage_list = [];
        self.fibroblast_list = []; 
        '''

    def step(self):
        self.schedule.step

# Create a CanvasGrid for visualization
def agent_portrayal(agent):
    portrayal = {}
    
    # Define the portrayal for the Endothelial agents
    if isinstance(agent, Endothelial):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1  # radius of the circle
        portrayal["Filled"] = "true"
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0  # Layer position on the grid
    
    # Add other agents' representations here if needed, e.g. Tumor_cells, M1, M2, etc.
    # elif isinstance(agent, Tumor_cells):
    #     portrayal["Shape"] = "rect"
    #     portrayal["w"] = 1
    #     portrayal["h"] = 1
    #     portrayal["Color"] = "red"
    #     portrayal["Layer"] = 1

    return portrayal

# Set up the visualization canvas
canvas_element = CanvasGrid(agent_portrayal, 125, 135, 600, 600)

# Create the ModularServer to run the visualization
server = ModularServer(MainModel, [canvas_element], "Endothelial Simulation")
server.port = 8521  # You can set a custom port

# Run the visualization server
server.launch()








#MAIN

#INITATE EMPTY MODEL
#model1 = MainModel()

#ADD AGENTS TO THE MODEL
#model1.generate_agents()

#RUN THE MODEL
#model1.run()


