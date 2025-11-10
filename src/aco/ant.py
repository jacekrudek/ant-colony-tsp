# in src/aco/ant.py
import random

class Ant:
    def __init__(self, colony):
        self.colony = colony
        self.problem = colony.problem

    def find_tour(self):
        """Builds a complete tour and returns it with its total length."""
        self.path = []
        # Keep track of which vertices are not yet visited
        self.visited = {vertice_idx: False for vertice_idx in range(self.problem.num_vertices)}
        
        # 1. Start at a random vertice
        current_vertice = random.randint(0, self.problem.num_vertices - 1)
        self.path.append(current_vertice)
        self.visited[current_vertice] = True

        # 2. Build path vertice by vertice
        while len(self.path) < self.problem.num_vertices:
            next_vertice = self._choose_next_vertice(current_vertice)
            self.path.append(next_vertice)
            self.visited[next_vertice] = True
            current_vertice = next_vertice
        
        # 3. Return to the start to complete the tour
        self.path.append(self.path[0])
        
        # 4. Calculate the total length of this path
        length = 0.0
        for i in range(len(self.path) - 1):
            vertice_a = self.path[i]
            vertice_b = self.path[i+1]
            length += self.problem.distance_matrix[vertice_a][vertice_b]
            
        return self.path, length

    def _choose_next_vertice(self, current_vertice):
        """Implements the ACO probability formula to select the next vertice."""
        pheromones = self.colony.pheromone_matrix
        distances = self.problem.distance_matrix
        alpha = self.colony.alpha
        beta = self.colony.beta

        probabilities = {}
        total_prob = 0.0

        # Calculate the numerator of the formula for all unvisited vertices
        for next_vertice in range(self.problem.num_vertices):
            if not self.visited[next_vertice]:
                distance = distances[current_vertice][next_vertice]
                if distance == 0: continue # Avoid division by zero if somehow at same vertice

                pheromone_level = pheromones[current_vertice][next_vertice] ** alpha
                heuristic_value = (1.0 / distance) ** beta
                prob = pheromone_level * heuristic_value
                
                probabilities[next_vertice] = prob
                total_prob += prob

        # --- Roulette Wheel Selection ---
        if total_prob == 0:
            # Failsafe: if all paths have 0 prob, just pick one at random
            return [vertice for vertice, visited in self.visited.items() if not visited][0]

        # Pick a random "slice" of the wheel
        r = random.uniform(0.0, total_prob)
        cumulative_prob = 0.0
        
        # Find which vertice "owns" that slice
        for vertice, prob in probabilities.items():
            cumulative_prob += prob
            if cumulative_prob >= r:
                return vertice
        
        # Failsafe (shouldn't be reached)
        return max(probabilities, key=probabilities.get)