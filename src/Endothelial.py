from mesa import Agent;
import random as random;
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
        if position > abs()
        # Define behaviour for diff situations here
        pass

    def proliferate(self):
        empty_cells = [cell for cell in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False) 
                       if self.model.grid.is_cell_empty(cell)]
        if empty_cells:
            if endo_type == "horizontal cell":
                x_inc = random.randint(0,1)
                y_inc = random.randint(-1,1)
                x_coord = 0
                y_coord = random.randrange(0, 1)
                new_position = self.choice(empty_cells)
                new_agent = Endothelial(self.model.next_id(), self.model)
                self.model.grid.place_agent(new_agent, new_position)
                self.model.schedule.add(new_agent)
            
            elif endo_type == "vertical cell":
                
                new_agent = Endothelial(self.model.next_id(), self.model)
                self.model.grid.place_agent(new_agent, new_position)
                self.model.schedule.add(new_agent)