import random

class Ant:
    def __init__(self):
        pass

    def find_tour(self, graph, pheromone_matrix, alpha, beta):
        self.graph = graph
        self.pheromone_matrix = pheromone_matrix
        self.alpha = alpha
        self.beta = beta

        self.path = []

        self.visited = []

        for _ in range(graph.num_vertices):
            self.visited.append(False)
        
        current_vertice = random.randint(0, graph.num_vertices - 1)

        self.path.append(current_vertice)

        self.visited[current_vertice] = True

        self.iterate_through_vertices(current_vertice)

        length = 0.0
        for i in range(len(self.path) - 1):
            vertice_a = self.path[i]
            vertice_b = self.path[i+1]
            length += self.graph.distance_matrix[vertice_a][vertice_b]

        return self.path, length

    def iterate_through_vertices(self, current_vertice):
        while len(self.path) < self.graph.num_vertices:
            next_vertice = self.choose_next_vertice(current_vertice)

            delta = self.graph.get_edge_grade(current_vertice, next_vertice)
            self.pheromone_matrix.add_pending(current_vertice, next_vertice, delta)

            self.path.append(next_vertice)
            self.visited[next_vertice] = True

            current_vertice = next_vertice

        self.path.append(self.path[0])
        delta = self.graph.get_edge_grade(current_vertice, self.path[0])
        self.pheromone_matrix.add_pending(current_vertice, self.path[0], delta)

    def choose_next_vertice(self, current_vertice):
        probabilities = {}
        total_prob = 0.0

        for next_vertice in range(self.graph.num_vertices):
            if not self.visited[next_vertice]:
                distance = self.graph.distance_matrix[current_vertice][next_vertice]

                pheromone_level = self.pheromone_matrix.current[current_vertice][next_vertice] ** self.alpha

                path_grade = (1.0 / distance) ** self.beta
                probability = pheromone_level * path_grade

                probabilities[next_vertice] = probability

                total_prob += probability

        r = random.uniform(0.0, total_prob)
        cumulative_prob = 0.0

        for vertice, prob in probabilities.items():
            cumulative_prob += prob

            if r <= cumulative_prob:
                return vertice
