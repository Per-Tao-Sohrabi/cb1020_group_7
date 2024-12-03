from mesa import Agent;
'''
# M1 class
### Desricption:
. . .


'''
class M1(Agent): # This class contains every action and interaction that the macrophages will have
    def __init__(self, unique_id, position, model): #Position inputed as (x,y)
        super().__init__(unique_id, model)
        self.position = position;
        self.killing_capacity = 11 #M1kmax
        self.prob_kill = 0.0306 #M1pkill
        self.prob_migrate = 0.2667 #M1pmig
        self.prob_death = 0.0049 #M1pdeath
        self.random_walk_influence = 0.8 #M1rwalk, vet inte om detta är relevant
        self.speed = 40 #M1speed, också ondöigt kanske
        self.engagement_duration = 60 #antal steg som immuna celler integerar

        self.engaged = 0 #hur länge agenten är upptagen
        self.kills_left = self.killing_capacity #antal dödanden kvar

        if self.engaged > 0: 
            pass #Försök att döda en tumörcell

        if self.random.random() < self.prob_migrate: #om inte engagerad så ska den flytta
            self.move()

    def move(self):
        #Makrofagern kommer att röra på sig slummässigt eller mot ett mål beroende på närvaro av signaler
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if self.random.random() < self.random_walk_influence:
            pass
    
    def step(self):
        #define behaviour for diff situations here
        pass
