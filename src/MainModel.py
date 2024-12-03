from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Tumor_cells import Tumor_cells; 
from M1 import M1;
from M2 import M2;
from Endothelial import Endothelial;
from Fibroblast import Fibroblast;

class MainModel(Model):
    #GENERATE AGENTS 
    def generate_agents(self, agent_type, amount):
        for i in range(amount):
            if agent_type == Endothelial:
                agent_type = agent_type;
                agent = agent_type(i, self) #declare new instance of agent according to mesa Agent initation.
                self.schedule.add(agent);
                #Create blodkärl on the grid.
                    #Add "next" endo besides prev endo
                pass #temporary
            else:
                #Generate Agents:
                agent_type = agent_type;
                agent = agent_type(i, self) #declare new instance of agent according to mesa Agent initation.
                self.schedule.add(agent);
                #Declare Agent Coordinates:
                x = self.random.randrange(self.grid.width);
                y = self.random.randrange(self.grid.height);
                self.grid.place_agent(agent, (x, y));
                i+=1
                #add the agents to the grid.
        
    #INSTANCE MODEL FIELDS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = MultiGrid(125, 135, torus=False);
        self.schedule = SimultaneousActivation(self);
        self.generate_agents(Tumor_cells,1);
        #self.generate_agents(Endothelial, 30);
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

#RUN MODEL SIMULATION
model = MainModel;






#MAIN

#INITATE EMPTY MODEL
#model1 = MainModel()

#ADD AGENTS TO THE MODEL
#model1.generate_agents()

#RUN THE MODEL
#model1.run()


