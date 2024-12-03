from mesa import Model
# from mesa import Agent, AgentSet; Obsolete
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from .Tumor_cells import Tumor_cells; 
from .M1 import M1;
from .M2 import M2;
from .Endothelial import Endothelial;
from .Fibroblast import Fibroblast;

class MainModel(Model):
    #GENERATE AGENTS 
    def generate_agents(self, agent_type, amount):
        if agent_type == "epithelial_cells" :
            #Create blodkärl on the grid.
                #Add "next" endo besides prev endo
            pass #temporary
        else:
            for i in range(amount):
                agent = agent_type(i, self) #declare new instance of agent according to mesa Agent initation.
                i+=1;
                #add the agents to the grid.
        
    #INSTANCE FIELDS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(125, 135, torus=False);

        self.generate_agents(cells,1);
        self.generate_agents(endo, 30);
        self.generate_agents(m1, 10);
        self.generate_agents(m2, 10);
        self.generate_agents(fib, 5);
    
        '''
        self.cell_list = [];
        self.macrophage_list = [];
        self.fibroblast_list = []; 
        '''




#MAIN

#INITATE EMPTY MODEL
model1 = MainModel()

#ADD AGENTS TO THE MODEL
model1.generate_agents(cells)

#RUN THE MODEL
#model1.run()


