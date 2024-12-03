from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
#from mesa.visualization.modules import CanvasGrid
#from mesa.visualization.ModularVisualization import ModularServer

# Fibroblast Agent
class Fibroblast(Agent):
    def __init__(self, unique_id, position, model): #Position inputed as (x,y)
        super().__init__(unique_id, model)
        self.position = position;
        self.alive = True
        self.proliferation_capacity = self.model.params["Fpmax"]

    def step(self):
        # Death
        if self.random.random() < self.model.params["Fpdeath"]:
            self.alive = False
            self.model.grid.remove_agent(self)
            return

        # Migration
        if self.random.random() < self.model.params["Fpmig"]:
            self.migrate()

        # Proliferation
        if self.proliferation_capacity > 0 and self.random.random() < self.model.params["Fpprol"]:
            self.proliferate()

    def migrate(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def proliferate(self):
        empty_cells = [cell for cell in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
                       if self.model.grid.is_cell_empty(cell)]
        if empty_cells:
            new_position = self.random.choice(empty_cells)
            new_agent = Fibroblast(self.model.next_id(), self.model)
            self.model.grid.place_agent(new_agent, new_position)
            self.model.schedule.add(new_agent)
            self.proliferation_capacity -= 1

'''
# Fibroblast Model
class FibroblastModel(Model):
    def __init__(self, width, height, initial_cell_ratio, params):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.params = params

        # Create initial fibroblasts
        num_agents = int(width * height * initial_cell_ratio)
        for i in range(num_agents):
            x, y = self.random.randrange(width), self.random.randrange(height)
            agent = Fibroblast(self.next_id(), self)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()


# Visualization Function
def fibroblast_portrayal(agent):
    return {"Shape": "circle", "Color": "blue", "Filled": True, "Layer": 0, "r": 0.5} if agent.alive else None


# Model Parameters
params = {
    "Fpprol": 0.0838,  # Probability of proliferation
    "Fpmig": 0.4,      # Probability of migration
    "Fpdeath": 0.0018, # Probability of death
    "Fpmax": 4         # Initial proliferation capacity
}

# Visualization
grid = CanvasGrid(fibroblast_portrayal, 20, 20, 500, 500)
server = ModularServer(FibroblastModel, [grid], "Fibroblast Model", {
    "width": 20,
    "height": 20,
    "initial_cell_ratio": 0.1,
    "params": params
})
server.port = 8521
server.launch()

'''