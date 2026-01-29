from mesa import Agent;



"""
    Initializes an Endothelial agent.

    Args:
        unique_id (int): A unique identifier for the agent.
        position (tuple): The (x, y) coordinates of the agent in the grid.
        model (object): The simulation model instance the agent belongs to.
        proliferation_prob (float): Probability of the agent to proliferate.
        targeted_prolif (tuple or None): The target coordinates for directed proliferation.
"""
class Endothelial(Agent):
    # STATIC FIELDS
    def get_class_name(self):
         return "Endothelial"

    def __init__(self, unique_id, position, model): # Position inputed as (x,y)
        super().__init__(unique_id, model)
        self.unique_id
        self.model = model
        self.position = position
        self.proliferation_prob = 100
        self.targeted_prolif = None
        self.nurish(5)

    '''  
        Initiates targeted proliferation based on a specific coordinate and induction factor.
    '''
    def targeted_proliferation(self, target_coord, induction_factor):
        #print(f'Endothelial position = {self.position}')
        self.targeted_prolif = target_coord
        x_target, y_target = target_coord
        self.proliferation_prob = 100*induction_factor
        
        # Create the new agent:
        if self.random.randint(0,100) < self.proliferation_prob:
            self.model.generate_agents(Endothelial, "directed proliferation", 1, self.position)
    
    '''
        Consumes a specified amount of nutrition from the model.
    '''
    def eat(self, val):
        self.model.eat_nutrition(val)
    
    '''
        Updates the model's nutrition capacity by a specified value.
    '''
    def nurish(self, val):
        self.model.update_nutrition_cap(val)
        #print("nurished")

    '''
        Adjusts the proliferation probability based on the nutritional state and cell density.
    '''
    def hunger(self):

        total_cells = self.model.grid.width*self.model.grid.height + self.model.data_collection("count", "total") 

        nutrition_count = self.model.nutrition_cap

        depletion_ratio = nutrition_count/total_cells

        self.proliferation_prob *= depletion_ratio

    '''
        Defines the behavior of the agent at each simulation step. It performs nourishment and consumes nutrition.
    '''
    def step(self):
        self.nurish(6)
        self.eat(1)
        #self.hunger()
        #define behaviour for diff situations here
        pass

    '''
    Only Grow if there is space in the three adjacent cells in the corners directed towards your target cell. 
    This means that only the first one that manages to grow into a cell is allowed to continue. 
    '''