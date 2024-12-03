from mesa import Model
from mesa.space import MultiGrid
from mesa import Agent
import random


#from mesa import Agent;
'''
# M2 class
### Desricption:
. . .


'''
class M2(Agent):
<<<<<<< HEAD
    def __init__(self, unique_id, position, model): #Position inputed as (x,y)
        super().__init__(unique_id, model)
        self.position = position;
=======
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model);

>>>>>>> 00e4e96e5f131cc137288e9484cf250cc26bc342
        self.killing_capacity = 11 #M2kmax
        self.prob_kill = 0.0127 #M2pkill
        self.prob_migrate = 0.2667 #M2pmig
        self.prob_death = 0.0049 #M2pdeath
        self.random_walk_influence = 0.8 #M2rwalk, vet inte om detta är relevant
        self.speed = 40 #M2speed, också ondöigt kanske
        self.engagement_duration = 60 #antal steg som immuna celler interagerar

        self.engaged = 0 #hur länge agenten är upptagen
        self.kills_left = self.killing_capacity #antal dödanden kvar
        #pass
 

    def step(self):
       """
       M2 macrophage action per step.
       Attempts to kill tumor cells in its vicinity.
       """
       neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
       for neighbor in neighbors:
           if isinstance(neighbor, TumorCell) and random.random() < self.killing_probability:
               self.model.grid.remove_agent(neighbor)
               self.kills_left -= 1
               break
           


#skapa en instans av agenten
#testa om agenten skapades


# Definiera TumorCell-agenten för att undvika referensproblem
class TumorCell(Agent):
   def __init__(self, unique_id, model):
       super().__init__(unique_id, model)
       self.type = "tumor"


# Testmodell
class TestModel(Model):
   def __init__(self, width, height):
       self.grid = MultiGrid(width, height, torus=True)
       self.schedule = None  # Valfritt om du inte behöver köra schemalagda steg


# Skapa en instans av modellen
model = TestModel(width=10, height=10)


# Skapa en instans av M2-agenten
m2_agent = M2(unique_id=1, model=model)


# Placera agenten på en specifik position i nätet
position = (5, 5)
model.grid.place_agent(m2_agent, position)


# Bekräfta att agenten har skapats och placerats
print(f"M2-agent skapad med ID {m2_agent.unique_id} på position {position}.")
print(f"Killing capacity: {m2_agent.killing_capacity}")