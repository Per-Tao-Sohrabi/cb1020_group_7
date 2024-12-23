from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random

class M2(Agent):
    
    """
        Initializes an M2 macrophage agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (Model): The model the agent belongs to.
            params (dict): Dictionary of model parameters.
    """
    def __init__(self, unique_id, position, model):
        super().__init__(unique_id, model)
        self.position = position
        self.prob_migrate = 0.4
        self.prob_death = 0.005
        self.prob_support_growth = 0.05
        #self.engagement_duration = params["M2engagement_duration"] #används inte i koden, tror inte vi behöver den
        self.supported_tumors = 0

    """
        Executes one step of the macrophage's behavior:
        - Checks if the macrophage dies.
        - Attempts to migrate to a neighboring cell.
        - Supports the growth of nearby tumor cells with a given probability.
    """
    def step(self):
        # Check if macrophage should die
        if random.random() < self.prob_death:
            self.model.grid.remove_agent(self)
            return

        # Attempt to migrate
        if random.random() < self.prob_migrate:
            self.random_move()

        
# Check neighbors for tumor cells
    def support_tumor_cells(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, TumorCell):
            # Support tumor growth with probability
                if random.random() < self.prob_support_growth:
                # Create a new tumor cell in a random neighboring position
                    empty_neighbors = self.model.grid.get_neighborhood(neighbor.pos, moore=True, include_center=False)
                    empty_neighbors = [pos for pos in empty_neighbors if self.model.grid.is_cell_empty(pos)]
                    if empty_neighbors:
                        new_tumor_cell = self.random.choice(empty_neighbors)
                        new_tumor_cell.set_proliferation_prob(1)
                        
    """
        Moves the macrophage to a random neighboring position.
    """
    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
