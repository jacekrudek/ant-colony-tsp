
import pygame

from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SCREEN_HEIGHT


class SidePanels:
    def __init__(self, small_font):
        self.small_font = small_font
        self.src_w = CENTER_WIDTH - 20
        self.src_h = SCREEN_HEIGHT - 20
        self.padding = 8

    def _draw_path_on_surface(self, surface, problem, path, color, top_offset):
        """Draw path inside surface, leaving top_offset pixels free for label."""
        if not path or len(path) < 2:
            return

        dst_w, dst_h = surface.get_size()
        pad = self.padding

        # compute drawable area below the label
        draw_y0 = top_offset + pad
        draw_h = max(1, dst_h - draw_y0 - pad)

        def map_point_local(x, y):
            sx = pad + (x / max(1, self.src_w)) * (dst_w - 2 * pad)
            sy = draw_y0 + (y / max(1, self.src_h)) * (draw_h)
            return int(sx), int(sy)

        pts = []
        for vidx in path:
            v = problem.vertices[vidx]
            pts.append(map_point_local(v.x, v.y))

        # draw segments and nodes (kept thin)
        for i in range(len(pts) - 1):
            pygame.draw.line(surface, color, pts[i], pts[i+1], 2)
        for p in pts:
            pygame.draw.circle(surface, (240,240,240), p, 2)

    def draw(self, target_surface, problem, colony, top_path_colors, best_color):
        """Draw 4 stacked panels at x=0 (left column)."""
        total_h = target_surface.get_height()
        panel_h = total_h // 4

        # label height (use font metrics + padding)
        label_text_height = self.small_font.get_height()
        label_h = max(20, label_text_height + 8)

        # fetch last iteration top paths
        last_paths = getattr(colony, "last_iteration_paths", []) or []
        sorted_paths = sorted(last_paths, key=lambda pl: pl[1]) if last_paths else []
        top_paths = sorted_paths[:3]

        # Panel 1: Best overall
        w1 = pygame.Surface((LEFT_PANEL_WIDTH, panel_h))
        w1.fill((25, 25, 35))

        # draw label background to avoid overlap
        pygame.draw.rect(w1, (20, 20, 30), pygame.Rect(0, 0, LEFT_PANEL_WIDTH, label_h))
        if getattr(colony, "best_path", None):
            self._draw_path_on_surface(w1, problem, colony.best_path, best_color, top_offset=label_h)
            label = f"Best overall: {colony.best_path_length:.2f}"
        else:
            label = "Best overall: -"
        # render label centered vertically in label area
        text_surf = self.small_font.render(label, True, (220,220,220))
        text_y = (label_h - self.small_font.get_height()) // 2
        w1.blit(text_surf, (8, text_y))
        target_surface.blit(w1, (0, 0))

        # Panels 2..4: top 1..3 of current iteration
        for i in range(3):
            wi = pygame.Surface((LEFT_PANEL_WIDTH, panel_h))
            wi.fill((25, 25, 35))
            y = (i + 1) * panel_h

            # label area background
            pygame.draw.rect(wi, (20, 20, 30), pygame.Rect(0, 0, LEFT_PANEL_WIDTH, label_h))

            if i < len(top_paths):
                path, length = top_paths[i]
                color = top_path_colors[i % len(top_path_colors)]
                self._draw_path_on_surface(wi, problem, path, color, top_offset=label_h)
                label = f"Iter top {i+1}: {length:.2f}"
            else:
                label = f"Iter top {i+1}: -"

            text_surf = self.small_font.render(label, True, (220,220,220))
            text_y = (label_h - self.small_font.get_height()) // 2
            wi.blit(text_surf, (8, text_y))
            target_surface.blit(wi, (0, y))