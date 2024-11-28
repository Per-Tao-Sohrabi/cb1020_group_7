from mesa import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
import Cells
import Macrophage_class as Macrophage

class MainModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(125, 135, torus=False);
        self.cell_list = [];
        self.macrophage_list = [];
        self.fibroblast_list = [];
    
    def generate_agents(self, agent_type, amount, agent_list):
        if agent_type == "epithelial_cells" :
            #Do something special
            print("In Construction")

            #Create nice blodkärl on the grid.
        else:
            for i in range(amount):
                agent = agent_type(i, self)
                agent_list.append(agent);
                i+=1;
                #add the agents to the grid.
#MAIN

#INITATE EMPTY MODEL
model1 = MainModel()

#ADD AGENTS TO THE MODEL
model1.generate_agents(cells)

#RUN THE MODEL
#model1.run()


