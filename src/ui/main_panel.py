import pygame

from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_PATH_COLORS, BEST_COLOR, PURPLE, PADDING


class MainPanel:
    def __init__(self):
        pass

    def _map_point(self, x, y, dst_w, dst_h):
        sx = PADDING + (x / max(1, CENTER_WIDTH - 20)) * (dst_w - 2 * PADDING)
        sy = PADDING + (y / max(1, SCREEN_HEIGHT - 20)) * (dst_h - 2 * PADDING)
        return int(sx), int(sy)

    def draw(self, target_surface, x_offset, aco):
        """Render center visualization and blit to target_surface at x_offset,0."""
        center_surf = pygame.Surface((CENTER_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        center_surf.fill((0, 0, 0, 0))

        # compute max pheromone
        max_ph = 0.0
        for row in aco.pheromone_matrix.current.values():
            for v in row.values():
                if v > max_ph:
                    max_ph = v
        if max_ph <= 0:
            max_ph = 1.0

        # draw all edges in purple with alpha/width based on pheromone
        for i in range(aco.graph.num_vertices):
            for j in range(i + 1, aco.graph.num_vertices):
                pher = aco.pheromone_matrix.current.get(i, {}).get(j, 0.0)
                norm = min(1.0, pher / max_ph)
                alpha = int(40 + 215 * norm)   # 40..255
                width = 1 + int(norm * 2)      # 1..3
                va = aco.graph.vertices[i]
                vb = aco.graph.vertices[j]
                p1 = self._map_point(va.x, va.y, CENTER_WIDTH, SCREEN_HEIGHT)
                p2 = self._map_point(vb.x, vb.y, CENTER_WIDTH, SCREEN_HEIGHT)
                col = (PURPLE[0], PURPLE[1], PURPLE[2], alpha)
                pygame.draw.line(center_surf, col, p1, p2, width)

        # draw highlighted best overall path (green) on top
        if getattr(aco.graph, "best_path", None):
            pts = []
            for vidx in aco.graph.best_path:
                v = aco.graph.vertices[vidx]
                pts.append(self._map_point(v.x, v.y, CENTER_WIDTH, SCREEN_HEIGHT))
            if len(pts) >= 2:
                pygame.draw.lines(center_surf, BEST_COLOR + (255,), False, pts, 3)

        # draw vertices on top
        for v in aco.graph.vertices:
            p = self._map_point(v.x, v.y, CENTER_WIDTH, SCREEN_HEIGHT)
            pygame.draw.circle(center_surf, (230, 230, 230, 255), p, 3)

        # blit to main surface
        target_surface.blit(center_surf, (x_offset, 0))