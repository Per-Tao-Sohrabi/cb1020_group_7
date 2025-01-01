from MainModel import MainModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Endothelial import Endothelial;
from Tumor_cells import Tumor_cells; 
from M1 import M1;
from M2 import M2;
from Fibroblast import Fibroblast;

def agent_portrayal(agent):
    """
    Define how agents are portrayed in the visualization.

    Args:
        agent (Agent): The agent to portray.

    Returns:
        dict: A portrayal dictionary specifying agent appearance.
"""
    portrayal = {
        "Filled": "true",   # Ensure the shape is filled
    }

    if isinstance(agent, Tumor_cells):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0

        # Add a label if multiple agents are in the same cell for clarity
        cell_contents = agent.model.grid.get_cell_list_contents(agent.position)
        if len(cell_contents) > 1:
            portrayal["text"] = f"{len(cell_contents)}"
            portrayal["text_color"] = "white"

    elif isinstance(agent, Endothelial):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0

    elif isinstance(agent, M1):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0

    elif isinstance(agent, M2):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
    
    elif isinstance(agent, Fibroblast):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0


    return portrayal

# Set up the visualization canvas
canvas_element = CanvasGrid(agent_portrayal, 150, 150, 1200, 1200) 

# Create the ModularServer to run the visualization
server = ModularServer(
    MainModel, 
    [canvas_element], 
    "Prostate Environment Simulation",
    model_params={"num_steps": 100}
)

server.port = 8521  # You can set a custom port
# Run the visualization server
server.launch()



