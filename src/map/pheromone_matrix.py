


class PheromoneMatrix:
    def __init__(self, vertex_count, evaporation_rate):

        self.vertex_count = vertex_count
        self.evaporation_rate = evaporation_rate
        self.current = self.init_pheromones(1.0)
        self.pending = self.init_pheromones(0.0)

    def init_pheromones(self, lvl):
        matrix = {}
        
        for i in range(self.vertex_count):
            matrix[i] = {}
            for j in range(self.vertex_count):
                if i != j:
                    matrix[i][j] = lvl
                else:
                  matrix[i][j] = 0.0
        
        return matrix
    
    def reset_pending(self):
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):

                self.pending[i][j] = 0.0

    def apply_pending(self):
        n = self.vertex_count
        pm = self.current
        pend = self.pending

        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                self.current[i][j] *= self.evaporation_rate

        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                self.current[i][j] += self.pending[i][j]

                self.pending[i][j] = 0.0

    def add_pending(self, i, j, delta):
        self.pending[i][j] += delta

