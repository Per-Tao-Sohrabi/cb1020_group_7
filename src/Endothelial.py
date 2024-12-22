from mesa import Agent;
'''
# Endothelial class
### Desricption:
. . .

'''
class Endothelial(Agent):
    #STATIC FIELDS
    def get_class_name(self):
        return "Endothelial"

    def __init__(self, unique_id, position, model): #Position inputed as (x,y)
        super().__init__(unique_id, model)
        self.unique_id
        self.model = model
        self.position = position
    
    def step(self):
        #define behaviour for diff situations here
        pass
