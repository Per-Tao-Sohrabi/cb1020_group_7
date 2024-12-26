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
        self.position = position;
        self.targeted_prolif = None

    def targeted_proliferation(self, target_coord):
        self.targeted_prolif = target_coord
        x_target, y_target = target_coord

        #Create the new agent:
        self.model.generate_agents(Endothelial, "directed proliferation", 1, self.position, self.targeted_prolif)

    def step(self):
            
        #define behaviour for diff situations here
        pass