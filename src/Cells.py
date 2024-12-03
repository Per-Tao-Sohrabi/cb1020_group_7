from mesa import Agent;
'''
# Cells class
### Description:
Objects of the Cells class can be cancerous or non-cancerous.
Cancerous cells have the possibility of inducing endothelial growth from the nearest endothelial cell towards the direction of the cancer cell. 
These cells might also only be cancerous. To be decided.
'''
class Cells(Agent):
    
    #Constructor

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model);
        self.unique_id = unique_id;
        #location

        #cancerous state

    #Growth method
    def step(self):
        #define behaviour for diff situations here
        pass
