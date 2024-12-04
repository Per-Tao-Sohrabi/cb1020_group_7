# READ ME
The SRC folder is meant to store all code files created throughout the project.

## Class Descriptions
### AgentClasses:
Each Agent Class needs to have a __init__(self) method, and a step(self) method. 
The step(self) method's purpose is to *define the behaviour of each agent instance during situations that it may encounter*. This can be done using if statements.

### MainModel:

### Instance Methods:
#### MainModel.generate_agents()
This method generates instances of specified agent types.
If the inputed agent type is endothelial, an attempt in craeting a continous line of blood endothelial cells is done. The first endothelial cell is placed (x=0, y=rand). Next endothelial is placed in any vertical or right side or diagonal adjacent cells.\
@param agent_type, amount\
@author Per Sohrabi

