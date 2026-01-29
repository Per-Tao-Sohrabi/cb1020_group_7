from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from Tumor_cells import Tumor_cells
import random



"""   
    Represents an M2 macrophage agent in the model. 
    M2 affect the tumor progression in a negative way by supporting tumor cell growth.

    Args:
        unique_id (int): Unique identifier for the agent.
        position (tuple): The (x, y) coordinates of the agent in the grid.
        model (object): The simulation model instance the agent belongs to.
        prob_migrate (float): Probability of the agent migrating to a neighboring cell.
        prob_death (float): Probability of the agent dying at each step of the simulation.
        prob_support_growth (float): Probability of the agent supporting the growth of nearby tumor cells.
        alive (bool): Indicates whether the agent is alive.
"""
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
    
    def eat(self, val):
        self.model.eat_nutrition(val)
    
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
        self.eat(5)
        #if self.random.random() < self.prob_death:
        #    self.alive = False
        #    self.model.grid.remove_agent(self)
        #    self.model.schedule.remove(self)
        #    return
        if self.random.random() < self.prob_migrate:
            self.migrate()
        if self.random.random() < self.prob_support_growth:
            self.support_tumor_cells()

        # Attempt to migrate
    def migrate(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        # Filter only empty positions
        empty_positions = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos)]

        # Pick an empty position if there are any
        if len(empty_positions) > 0:
            new_position = self.random.choice(empty_positions)
            self.model.grid.move_agent(self, new_position)

        
# Check neighbors for tumor cells
    def support_tumor_cells(self):
        neighbors = self.model.grid.get_neighbors(self.position, moore=True, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, Tumor_cells):
            # Support tumor growth with probability
                if self.random.random() < self.prob_support_growth:
                # Create a new tumor cell in a random neighboring position
                    neighbors = self.model.grid.get_neighborhood(neighbor.position, moore=True, include_center=False)
                    tumor_cells = [cell for cell in neighbors if isinstance(cell, Tumor_cells)]
                    if tumor_cells:
                        tumor_cell = self.random.choice(tumor_cells) 
                        tumor_cell.set_proliferation_prob(2, "proportion")
                        tumor_cell.set_death_prob(0,"value")
                    
                    for agent in tumor_cells:
                        agent.set_angiogenesis_intensity(1)
    
    """
        Moves the macrophage to a random neighboring position.
    """
    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.position, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
