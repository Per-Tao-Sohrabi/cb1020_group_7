import random

class Fibroblast:
    def __init__(self, position, proliferation_capacity):
        self.position = position  # (x, y) for 2D space
        self.proliferation_capacity = proliferation_capacity
        self.alive = True

    def proliferate(self, prob):
        """Determine if fibroblast will divide."""
        if self.alive and self.proliferation_capacity > 0 and random.random() < prob:
            self.proliferation_capacity -= 1
            return True  # New cell should be created
        return False

    def migrate(self, prob, random_walk_factor, grid_size):
        """Move the fibroblast based on migration probability."""
        if self.alive and random.random() < prob:
            dx = random.randint(-1, 1) * random_walk_factor
            dy = random.randint(-1, 1) * random_walk_factor
            new_x = max(0, min(self.position[0] + dx, grid_size - 1))
            new_y = max(0, min(self.position[1] + dy, grid_size - 1))
            self.position = (new_x, new_y)

    def die(self, prob):
        """Kill the fibroblast based on death probability."""
        if self.alive and random.random() < prob:
            self.alive = False


class Simulation:
    def __init__(self, params, grid_size):
        self.params = params
        self.grid_size = grid_size
        self.agents = self.initialize_agents()

    def initialize_agents(self):
        """Create initial fibroblast population."""
        num_agents = int(self.params['FcellNo'] * self.grid_size**2)
        agents = []
        for _ in range(num_agents):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            agents.append(Fibroblast((x, y), self.params['Fpmax']))
        return agents

    def run_step(self):
        """Run a single time step of the simulation."""
        new_agents = []
        for agent in self.agents:
            agent.migrate(self.params['Fpmig'], self.params['Frwalk'], self.grid_size)
            if agent.proliferate(self.params['Fpprol']):
                # Create a new fibroblast at the same location as the parent
                new_agents.append(Fibroblast(agent.position, self.params['Fpmax']))
            agent.die(self.params['Fpdeath'])

        # Add new agents to the population
        self.agents.extend(new_agents)
        # Remove dead agents
        self.agents = [agent for agent in self.agents if agent.alive]

    def run(self, steps):
        """Run the simulation for a given number of steps."""
        for step in range(steps):
            self.run_step()
            print(f"Step {step + 1}: {len(self.agents)} agents alive.")


# Example Parameters
params = {
    'Fpprol': 0.0838,  # Probability of proliferation
    'Fpmig': 0.4,      # Probability of migration
    'Fpdeath': 0.0018, # Probability of death
    'Fpmax': 4,        # Initial proliferation capacity
    'Frwalk': 0.5,     # Random movement factor
    'FcellNo': 0.1     # Initial cell ratio (10% of grid space)
}

# Run Simulation
sim = Simulation(params, grid_size=125)
sim.run(steps=100)

