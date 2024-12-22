from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class M1(Agent):
    def __init__(self, agent_id, position, model):
        super().__init__(agent_id, model)
        self.position = position
        self.killing_capacity = 11       # Killing capacity 
        self.prob_kill = 0.03            # Probability of killing
        self.prob_migrate = 0.4          # Probability of migration
        self.prob_death = 0.005          # Probability of death
        self.alive = True

    def step(self):
        if not self.alive:
            return

        if self.random.random() < self.prob_death:
            self.alive = False
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        if self.random.random() < self.prob_migrate:
            self.migrate()

        if self.random.random() < self.prob_kill:
            self.kill_tumor_cell()

    def migrate(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)

    def kill_tumor_cell(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        tumor_cells = [cell for cell in neighbors if isinstance(cell, Tumor_cells)]
        if tumor_cells:
            target = self.random.choice(tumor_cells)
            self.model.grid.remove_agent(target)
            self.model.schedule_cell.remove(target)
            self.killing_capacity -= 1
'''
# Main Model
class MacrophageModel(Model):
    def __init__(self, width, height, initial_m1, params):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.params = params

        # Add M1 Macrophages
        for i in range(initial_m1):
            x, y = self.random.randrange(width), self.random.randrange(height)
            m1 = M1Macrophage(self.next_id(), self)
            self.grid.place_agent(m1, (x, y))
            self.schedule.add(m1)

    def step(self):
        self.schedule.step()


# Visualization Function
def portray_agent(agent):
    if isinstance(agent, M1Macrophage):
        return {"Shape": "circle", "Color": "red", "Filled": True, "Layer": 0, "r": 0.5} if agent.alive else None


# Model Parameters
params = {
    "M1kmax": 11,       # Killing capacity (not relevant here)
    "M1pmig": 0.4,      # Probability of migration
    "M1pdeath": 0.005,   # Probability of death
    "M1pkill": 0.03     # Probability of killing
}

# Visualization
grid = CanvasGrid(portray_agent, 20, 20, 500, 500)
server = ModularServer(MacrophageModel, [grid], "Macrophage Model", {
    "width": 20,
    "height": 20,
    "initial_m1": 10,
    "params": params
})
server.port = 8527
server.launch() '''
