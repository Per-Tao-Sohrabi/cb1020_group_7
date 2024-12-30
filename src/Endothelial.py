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

    def targeted_proliferation(self, target_coord, induction_factor):
        #print(f'Endothelial position = {self.position}')
        self.targeted_prolif = target_coord
        x_target, y_target = target_coord
        prol_prob = 100*induction_factor
        #Create the new agent:
        if self.random.randint(0,100) < prol_prob:
            self.model.generate_agents(Endothelial, "directed proliferation", 1, self.position)

    def step(self):
            
        #define behaviour for diff situations here
        pass


    '''
    Only Grow if there is space in the three adjacent cells in the corners directed towards your target cell. 
    This means that only the first one that manages to grow into a cell is allowed to continue. 
    '''