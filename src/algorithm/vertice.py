# in src/aco/vertice.py
import math

class Vertice:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other_vertice):
        dx = self.x - other_vertice.x
        dy = self.y - other_vertice.y
        return math.sqrt(dx*dx + dy*dy)