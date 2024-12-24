from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from Tumor_cells import Tumor_cells
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
        self.alive = True
    
    """
        Executes one step of the macrophage's behavior:
        - Checks if the macrophage dies.
        - Attempts to migrate to a neighboring cell.
        - Supports the growth of nearby tumor cells with a given probability.
    """
    def step(self):
        # Check if macrophage should die
        if not self.alive:
            return
        if self.random.random() < self.prob_death:
            self.alive = False
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return
        if self.random.random() < self.prob_migrate:
            self.migrate()
        if self.random.random() < self.prob_support_growth:
            self.support_tumor_cells()

        # Attempt to migrate
    def migrate(self):
        possible_steps = self.model.grid.get_neighborhood(self.position, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)

        
# Check neighbors for tumor cells
    def support_tumor_cells(self):
        neighbors = self.model.grid.get_neighbors(self.position, moore=True, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, Tumor_cells):
            # Support tumor growth with probability
                if self.random.random() < self.prob_support_growth:
                # Create a new tumor cell in a random neighboring position
                    empty_neighbors = self.model.grid.get_neighborhood(neighbor.position, moore=True, include_center=False)
                    empty_neighbors = [pos for pos in empty_neighbors if self.model.grid.is_cell_empty(pos)]
                    if empty_neighbors:
                        new_tumor_cell = self.random.choice(empty_neighbors)
                        new_tumor_cell.set_proliferation_prob(1)
                        
    """
        Moves the macrophage to a random neighboring position.
    """
    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.position, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
