# Här tänker jag att klassen för makrofag M1 & M2 ska vara.

class MacrophageM1: # This class contains every action and interaction that the macrophages will have
    def __init__(self, positions): # The attributen from...
        self.positions = positions # Lista med M1-makrofagernas positioner

    def (self, env, kill_prob): # Här använder jag env, men detta kommer nog behöva ändras baserat på vad vi gör i enviroment klassen tror jag
        new_positions =[]
        for m1 in self.positions:
            #Hitta grannar
            neighbors = [
                (m1[0] + dx, m1[1] + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1] 
                if 0 <= m1[0] + dx < env.grid_size and 0 <= m1[1] + dy < env.grid_size
            ]
        # Hitta tumörceller i närheten
        tumor_neighbors = [pos for pos in neighbors if env.grid[pos] == 1]

        #Försök döda en tumörcell
        if tumor_neighbors and np.random.rand() < kill_prob:
            kill_pos = tumor_neighbors[0] #Ta första tumörcellen
            env.grid[kill_pos] = 0 #Ta bort tumörcellen

        else:
            new_positions.append(m1)

    self.positions = new_positions #Uppdatera makrofagposition
       
    
