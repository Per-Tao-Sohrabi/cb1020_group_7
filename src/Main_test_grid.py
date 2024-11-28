




class Main_simulation(Model):
    def __init__(self, width, height):
        self.grid = Grid(width, height, torus=False) # torus = False 
        self.schedule = RandomActivation(self)       # activates each agent randomly one time per step in the simulation
        self.agent_ID = 0                            # Creates unique identification "agent_ID" for each agent in every iteration
        self.run_ABM = True

        # Place the initial tumour cell in the grid
        initial_tumor = TumorCell(self.next_id(), self)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(initial_tumor, (x, y))
        self.schedule.add(initial_tumor)

        # Datainsamling
        self.datacollector = DataCollector(
            model_reporters={"TumorCellCount": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, TumorCell))}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def next_id(self):
        self.agent_ID += 1
        return self.agent_ID


def run_AMBsim(width=125, height=125, steps=1000): # This function runs the whole simulation 
    simulation_run = Main_simulation(width, height)
    for _ in range(steps):
        simulation_run.step()
    return model.datacollector.get_model_vars_dataframe()

if __name__ == "__main__":
    results = run_ABMsim()
    print(results)










# Skräpkod 
import mesa as ms
class MainModel:

    def __init__(self, macrophage, fibroblast, cells):
        #Fields
        
        #lista för macrophages
        macList = [];
        fibList = [];
        cells = [];
        endothelial = [];