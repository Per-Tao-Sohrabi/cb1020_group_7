from mesa import Agent;
'''
# M2 class
### Desricption:
. . .


'''
class M2(Agent):
    def __init__(self, unique_id, model):
        super.__init__(unique_id, model);

        self.killing_capacity = 11 #M2kmax
        self.prob_kill = 0.0127 #M2pkill
        self.prob_migrate = 0.2667 #M2pmig
        self.prob_death = 0.0049 #M2pdeath
        self.random_walk_influence = 0.8 #M2rwalk, vet inte om detta är relevant
        self.speed = 40 #M2speed, också ondöigt kanske
        self.engagement_duration = 60 #antal steg som immuna celler interagerar

        self.engaged = 0 #hur länge agenten är upptagen
        self.kills_left = self.killing_capacity #antal dödanden kvar
        pass
 

    def step(self):
       """
       M2 macrophage action per step.
       Attempts to kill tumor cells in its vicinity.
       """
       neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
       for neighbor in neighbors:
           if isinstance(neighbor, TumorCell) and random.random() < self.killing_probability:
               self.model.grid.remove_agent(neighbor)
               break


