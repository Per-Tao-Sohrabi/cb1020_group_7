from mesa import Agent, Model

# # OBS: Varje klass som hör till en unik cell-typ bör vara i en separat fil sen (nu är dem här för att kunna testköra koden)
# class Macrophage_M1(TU_Cell_Agent): 
#     def __init__(self, agent_id, model, "Macrophage_M1"):
#         self.anti_cancerous = False
#         self.proliferation_prob = 0.0065
#         # etc. lägg till flera instansvariabler
        
# class Fibroblast(TU_Cell_Agent):
#     def __init__(self, agent_id, model, "Fibroblast"):
#         # Samma här, addera instansvariabler

# class Endothelial(TU_Cell_Agent):
#     def __init__(self, agent_id, model, "Endothelial"):
#         self.proliferation_prob = 0.02





# The main class definies the key-parameters for the run of the ABM prostate cancer simulation
    """
    Main simulation class for prostate cancer ABM.

    Attributes:
        grid (MultiGrid): 2D grid where agents are placed.
        schedule_cell (RandomActivation): Scheduler for agent activation.
        agent_id (int): Counter for unique agent IDs.
        run_ABM (bool): Flag to control simulation runtime.
        datacollector (DataCollector): Collects data during the simulation.
    """
class Main_simulation(Model):
      """
        Initialize the simulation model.

        Args:
            width (int): Width of the simulation grid.
            height (int): Height of the simulation grid.
        """
    def __init__(self, width, height):
        super().__init__()
        self.grid = MultiGrid(width, height, True)   # Creates a 2D-grid
        self.schedule_cell = RandomActivation(self)  # Activates each agent randomly one time per step in the simulation
        self.agent_id = 0                            # Creates unique identification "agent_ID" for each agent in every iteration
        self.run_ABM = True                          # Runs the AMB-simulation

        # Place the initial tumour cell in the grid
        initial_tumor = Tumor_Cell(self.agent_id, self)   # Creates a new instance of the class Tumor_Cell 
        x = self.random.randrange(self.grid.width)        # Creates a random x-coordinate within the grid's width
        y = self.random.randrange(self.grid.height)       # Creates a random y-coordinate within the grid's width
        self.grid.place_agent(initial_tumor, (x, y))      # Places the agent in the correct place
        self.schedule_cell.add(initial_tumor)
        

        # Collects the data for how many tumor cells we have
        self.datacollector = DataCollector(
            model_reporters={"Number_tumor_Cells": lambda m: sum(1 for agent in m.schedule_cell.agents if isinstance(agent, Tumor_Cell))}
        )
  """
        Advance the simulation by one step, collecting data and activating agents.
        """
    def step(self):                                       # This method takes steps in the simulation
    
        self.datacollector.collect(self)                  # It collects all the required data as well
        self.schedule_cell.step()                         
"""
        Generate a unique ID for a new agent.

        Returns:
            int: Unique agent ID.
        """
    def next_agent_id(self):                              # Keeps track of the "agent_id", crucial for knowing the composition of the cells in the end
        self.agent_id += 1
        return self.agent_id


# This function runs the whole simulation 
   """
    Run the ABM simulation and return collected data.

    Args:
        width (int): Width of the grid.
        height (int): Height of the grid.
        steps (int): Number of simulation steps.

    Returns:
        DataFrame: Simulation results with collected data.
    """
def run_ABM_sim(width=125, height=125, steps=100): 
    model = Main_simulation(width, height)
    for _ in range(steps):
        model.step()
    return model.datacollector.get_model_vars_dataframe()

if __name__ == "__main__":
    results = run_ABM_sim()
    print(results)

# The main class code is finished here!!






