from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.visualization.modules import CanvasGrid
# from mesa.visualization.ModularVisualization import ModularServer

# Fibroblast Agent
"""
    Represents a fibroblast agent in the model.

    Attributes:
        position (tuple): The (x, y) position of the agent in the grid.
        alive (bool): Indicates whether the agent is alive.
        proliferation_capacity (int): The remaining capacity for the agent to proliferate.
"""

# Define parameters for the Fibroblast agent
params = {
    "Fpdeath": 0.0018,  # Probability of death
    "Fpmig": 0.4,       # Probability of migration
    "Fpprol": 0.0838,    # Probability of proliferation
    "Fpmax": 4           # Initial proliferation capacity
}

class Fibroblast(Agent):
    """
        Initializes a Fibroblast agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            position (tuple): Initial position of the agent in the grid (x, y).
            model (Model): The model the agent belongs to.
    """
    def __init__(self, unique_id, position, model):
        super().__init__(unique_id, model)
        self.position = position
        self.alive = True
        self.proliferation_capacity = params["Fpmax"]

    """
        Executes one step for the fibroblast agent, including:
        - Death: Agent may die based on the `Fpdeath` probability.
        - Migration: Agent may move to a neighboring cell based on the `Fpmig` probability.
        - Proliferation: Agent may create a new fibroblast in an adjacent cell if it has 
        proliferation capacity and the `Fpprol` probability is met.
    """
    def step(self):
        # Death
        if self.random.random() < params["Fpdeath"]:
            self.alive = False
            self.model.grid.remove_agent(self)
            return

        # Migration
        if self.random.random() < params["Fpmig"]:
            self.migrate()

        # Proliferation
        if self.proliferation_capacity > 0 and self.random.random() < params["Fpprol"]:
            self.proliferate()

    """
        Moves the agent to a random neighboring cell if possible.
    """
    def migrate(self):
        possible_steps = self.model.grid.get_neighborhood(self.position, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    """
        Creates a new fibroblast agent in an empty neighboring cell if one exists.
        Reduces the proliferation capacity of the current agent by 1.
    """
    def proliferate(self):
        empty_cells = [cell for cell in self.model.grid.get_neighborhood(self.position, moore=True, include_center=False)
                       if self.model.grid.is_cell_empty(cell)]
        if empty_cells:
            new_position = self.random.choice(empty_cells)
            new_agent = Fibroblast(self.model.next_id(), new_position, self.model)
            self.model.grid.place_agent(new_agent, new_position)
            self.model.schedule.add(new_agent)
            self.proliferation_capacity -= 1


# Fibroblast Model
class FibroblastModel(Model):
    """
        Initializes the FibroblastModel, which contains the grid, the scheduler, and the parameters.

        Args:
            width (int): Width of the grid.
            height (int): Height of the grid.
            initial_cell_ratio (float): Ratio of initial fibroblasts to grid size.
            params (dict): Dictionary of parameters for the Fibroblast agent.
    """
    def __init__(self, width, height, initial_cell_ratio, params):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.params = params

        # Create initial fibroblasts
        num_agents = int(width * height * initial_cell_ratio)
        for i in range(num_agents):
            x, y = self.random.randrange(width), self.random.randrange(height)
            agent = Fibroblast(self.next_id(), (x, y), self)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


# Visualization Function
def fibroblast_portrayal(agent):
    """
        Function to portray a fibroblast agent for visualization.

        Args:
            agent (Fibroblast): The fibroblast agent to be portrayed.
        
        Returns:
            dict: A dictionary of visualization parameters for the agent.
    """
    return {"Shape": "circle", "Color": "blue", "Filled": True, "Layer": 0, "r": 0.5} if agent.alive else None


# Model Parameters
params = {
    "Fpprol": 0.0838,  # Probability of proliferation
    "Fpmig": 0.4,      # Probability of migration
    "Fpdeath": 0.0018, # Probability of death
    "Fpmax": 4         # Initial proliferation capacity
}

# Visualization
# Uncomment these lines if you are setting up a visualization server
# grid = CanvasGrid(fibroblast_portrayal, 20, 20, 500, 500)
# server = ModularServer(FibroblastModel, [grid], "Fibroblast Model", {
#     "width": 20,
#     "height": 20,
#     "initial_cell_ratio": 0.1,
#     "params": params
# })
# server.port = 8521
# server.launch()
