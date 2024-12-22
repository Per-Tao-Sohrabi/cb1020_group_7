from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random


# Tumor Cell Class
"""
    Represents a tumor cell in the model.

    Attributes:
        size (float): The current size of the tumor cell.
    """
class TumorCell(Agent):
    
    """
        Initializes a TumorCell agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (Model): The model the agent belongs to.
        """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.size = 1  # Tumor starts with size 1
    
    """
        Executes one step of the tumor cell's behavior:
        - Increases its size by a fixed growth rate.
        - Randomly moves to a neighboring cell.
        """
    def step(self):
        # Tumor grows independently at a base rate
        self.size += 0.1
        self.random_move()

    """
        Moves the tumor cell to a random neighboring position.
        """
    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

# kanske behöver ändras beroende på vad main har osv, men använde detta bara för att kunna köra
# M2 Macrophage Class

"""
    Represents an M2 macrophage in the model.

    Attributes:
        killing_capacity (int): Maximum number of tumor cells the agent can kill (unused).
        prob_migrate (float): Probability of migrating to a new position in a step.
        prob_death (float): Probability of dying in a step.
        prob_support_growth (float): Probability of supporting tumor cell growth in a step.
        supported_tumors (int): Counter for the number of tumors supported by this macrophage.
        kills_left (int): Remaining kills before the macrophage reaches its killing capacity.
    """
class M2Macrophage(Agent):
    
    """
        Initializes an M2 macrophage agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (Model): The model the agent belongs to.
            params (dict): Dictionary of model parameters.
        """
    def __init__(self, unique_id, model, params):
        super().__init__(unique_id, model)
        self.killing_capacity = params["M2kmax"] # osäker på vad vi gör med denna
        self.prob_migrate = params["M2pmig"]
        self.prob_death = params["M2pdeath"]
        self.prob_support_growth = params["M2psupport_growth"]
        self.engagement_duration = params["M2engagement_duration"] #används inte i koden, tror inte vi behöver den
        self.supported_tumors = 0
        self.kills_left = self.killing_capacity

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
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, TumorCell):
                # Support tumor growth with probability
                if random.random() < self.prob_support_growth:
                    neighbor.size += 0.2
                    self.supported_tumors += 1

    """
        Moves the macrophage to a random neighboring position.
        """
    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

# Cancer Growth Model
"""
    Represents the cancer growth model with tumor cells and M2 macrophages.

    Attributes:
        grid (MultiGrid): The spatial grid where agents are placed.
        schedule (RandomActivation): Scheduler to manage agent activation.
        params (dict): Dictionary of model parameters.
        agent_id (int): Counter to assign unique IDs to agents.
    """
class CancerModel(Model):
    """
        Initializes the cancer growth model.

        Args:
            width (int): Width of the grid.
            height (int): Height of the grid.
            initial_m2 (int): Number of initial M2 macrophages.
            initial_tumors (int): Number of initial tumor cells.
            params (dict): Dictionary of model parameters.
        """
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

    """
        Advances the model by one step.
        """
    def step(self):
        self.schedule.step()

    """
        Generates the next unique ID for a new agent.

        Returns:
            int: The next unique agent ID.
        """
    def next_agent_id(self):
        self.agent_id += 1
        return self.agent_id


"""
    Returns a dictionary for visualizing an agent.

    Args:
        agent (Agent): The agent to portray.

    Returns:
        dict: Dictionary containing visualization properties of the agent.
    """
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


