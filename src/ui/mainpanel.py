import pygame

class MainPanel:
    def __init__(self, width, height, src_w, src_h, purple=(150, 80, 200), best_color=(0, 255, 0), padding=8):
        self.width = width
        self.height = height
        self.src_w = src_w
        self.src_h = src_h
        self.purple = purple
        self.best_color = best_color
        self.padding = padding

    def _map_point(self, x, y, dst_w, dst_h):
        pad = self.padding
        sx = pad + (x / max(1, self.src_w)) * (dst_w - 2 * pad)
        sy = pad + (y / max(1, self.src_h)) * (dst_h - 2 * pad)
        return int(sx), int(sy)

    def draw(self, target_surface, x_offset, problem, colony):
        """Render center visualization and blit to target_surface at x_offset,0."""
        center_surf = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        center_surf.fill((0, 0, 0, 0))

        # compute max pheromone
        max_ph = 0.0
        for row in colony.pheromone_matrix.values():
            for v in row.values():
                if v > max_ph:
                    max_ph = v
        if max_ph <= 0:
            max_ph = 1.0

        # draw all edges in purple with alpha/width based on pheromone
        for i in range(problem.num_vertices):
            for j in range(i + 1, problem.num_vertices):
                pher = colony.pheromone_matrix.get(i, {}).get(j, 0.0)
                norm = min(1.0, pher / max_ph)
                alpha = int(40 + 215 * norm)   # 40..255
                width = 1 + int(norm * 2)      # 1..3
                va = problem.vertices[i]
                vb = problem.vertices[j]
                p1 = self._map_point(va.x, va.y, self.width, self.height)
                p2 = self._map_point(vb.x, vb.y, self.width, self.height)
                col = (self.purple[0], self.purple[1], self.purple[2], alpha)
                pygame.draw.line(center_surf, col, p1, p2, width)

        # draw highlighted best overall path (green) on top
        if getattr(colony, "best_path", None):
            pts = []
            for vidx in colony.best_path:
                v = problem.vertices[vidx]
                pts.append(self._map_point(v.x, v.y, self.width, self.height))
            if len(pts) >= 2:
                pygame.draw.lines(center_surf, self.best_color + (255,), False, pts, 3)

        # draw vertices on top
        for v in problem.vertices:
            p = self._map_point(v.x, v.y, self.width, self.height)
            pygame.draw.circle(center_surf, (230, 230, 230, 255), p, 3)

        # blit to main surface
        target_surface.blit(center_surf, (x_offset, 0))