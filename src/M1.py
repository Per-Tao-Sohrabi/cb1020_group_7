from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from Tumor_cells import Tumor_cells
from mesa.visualization.ModularVisualization import ModularServer



"""
    Represents an M1 macrophage agent in the model. 
    M1 affects the tumor progression in a positive manner by killing tumor cells.

    Args:
        position (tuple): The (x, y) position of the agent in the grid.
        killing_capacity (int): The number of tumor cells the agent can kill.
        prob_kill (float): Probability of killing a tumor cell in a step.
        prob_migrate (float): Probability of moving to a new position in a step.
        prob_death (float): Probability of dying in a step.
        alive (bool): Indicates whether the agent is alive.
"""
class M1(Agent):
    
    """
        Initializes an M1 macrophage agent.

        Args:
            agent_id (int): Unique identifier for the agent.
            position (tuple): Initial position of the agent in the grid.
            model (Model): The model the agent belongs to.
    """
    def __init__(self, agent_id, position, model):
        super().__init__(agent_id, model)
        self.position = position
        self.killing_capacity = 11       # Killing capacity 
        self.prob_kill = 0.0306          # Probability of killing
        self.prob_migrate = 0.2667       # Probability of migration
        self.prob_death = 0.0049         # Probability of death
        self.alive = True
    
    def eat(self, val):
        self.model.eat_nutrition(val)
    
    """
        Executes one step of the agent's behavior:
            - Checks if the agent dies based on `prob_death`.
            - Migrates to a neighboring cell with `prob_migrate`.
            - Attempts to kill a tumor cell in its neighborhood with `prob_kill`.
    """
    def step(self):
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
        if self.random.random() < self.prob_kill:
            self.kill_tumor_cell()
    
    """
        Moves the agent to a random neighboring cell if the new cell is empty.
    """
    def migrate(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        # Filter only empty positions
        empty_positions = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos)]

        # Pick an empty position if there are any
        if len(empty_positions) > 0:
            new_position = self.random.choice(empty_positions)
            self.model.grid.move_agent(self, new_position)

    """
        Kills a neighboring tumor cell if one exists.
        Reduces the killing capacity of the agent by 1.
    """
    def kill_tumor_cell(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        tumor_cells = [cell for cell in neighbors if isinstance(cell, Tumor_cells)]
        if tumor_cells:
            target = self.random.choice(tumor_cells)
            target.apoptosis() # set_death_prob(1, "val") # Before TC.apoptosis() was called raising NoneType Error
            self.killing_capacity -= 1

