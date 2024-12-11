from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random


#Tumor Cell Class
class TumorCell(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.size = 1  # Tumor starts with size 1

    def step(self):
        # Tumor grows independently at a base rate
        self.size += 0.1
        self.random_move()

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

 #kanske behöver ändras beroende på vad main har osv, men använde detta bara för att kunna köra
# M2 Macrophage Class
class M2Macrophage(Agent):
    def __init__(self, unique_id, model, params):
        super().__init__(unique_id, model)
        self.killing_capacity = params["M2kmax"] #osäker på vad vi gör med denna
        self.prob_migrate = params["M2pmig"]
        self.prob_death = params["M2pdeath"]
        self.prob_support_growth = params["M2psupport_growth"]
        self.engagement_duration = params["M2engagement_duration"] #används inte i koden, tror inte vi behöver den
        self.supported_tumors = 0
        self.kills_left = self.killing_capacity

    def step(self):
        # Check if macrophage should die
        if random.random() < self.prob_death:
            self.model.grid.remove_agent(self)
            return

        # Attempt to migrate
        if random.random() < self.prob_migrate:
            self.random_move()

        # Check neighbors for tumor cells
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, TumorCell):
                # Support tumor growth with probability
                if random.random() < self.prob_support_growth:
                    neighbor.size += 0.2
                    self.supported_tumors += 1

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


# Cancer Growth Model
class CancerModel(Model):
    def __init__(self, width, height, initial_m2, initial_tumors, params):
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.params = params
        self.agent_id = 0

        # Add initial Tumor Cells
        for _ in range(initial_tumors):
            tumor = TumorCell(self.next_agent_id(), self)
            x = random.randrange(width)
            y = random.randrange(height)
            self.grid.place_agent(tumor, (x, y))
            self.schedule.add(tumor)

        # Add initial M2 Macrophages
        for _ in range(initial_m2):
            m2 = M2Macrophage(self.next_agent_id(), self, params)
            x = random.randrange(width)
            y = random.randrange(height)
            self.grid.place_agent(m2, (x, y))
            self.schedule.add(m2)

    def step(self):
        self.schedule.step()

    def next_agent_id(self):
        self.agent_id += 1
        return self.agent_id


# Visualization Function
def portray_agent(agent):
    if isinstance(agent, TumorCell):
        return {
            "Shape": "circle",
            "Color": "blue",  # Tumor cells are blue
            "Filled": True,
            "Layer": 0,
            "r": min(agent.size / 10, 1)  # Size scales with tumor size
        }
    elif isinstance(agent, M2Macrophage):
        return {
            "Shape": "circle",
            "Color": "green",  # M2 macrophages are green
            "Filled": True,
            "Layer": 1,
            "r": 0.5
        }


# Parameters
params = {
    "M2kmax": 11,          # Killing capacity (not relevant here)
    "M2pmig": 0.4,         # Probability of migration
    "M2pdeath": 0.005,     # Probability of death
    "M2psupport_growth": 0.05,  # Probability of supporting tumor growth
    "M2engagement_duration": 5  # Engagement duration (optional)
}

# Visualization Setup
grid = CanvasGrid(portray_agent, 20, 20, 500, 500)
server = ModularServer(
    CancerModel,
    [grid],
    "Cancer Growth Model with M2 Macrophages",
    {
        "width": 20,
        "height": 20,
        "initial_m2": 5,
        "initial_tumors": 3,
        "params": params
    }
)
server.port = 8527
server.launch()

