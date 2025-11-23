
import pygame

from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SCREEN_HEIGHT, SMALL_FONT


class SidePanels:
    def __init__(self):
        self.src_w = CENTER_WIDTH - 20
        self.src_h = SCREEN_HEIGHT - 20
        self.padding = 8

    def _draw_path_on_surface(self, surface, aco, path, color, top_offset):
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
            v = aco.graph.vertices[vidx]
            pts.append(map_point_local(v.x, v.y))

        # draw segments and nodes (kept thin)
        for i in range(len(pts) - 1):
            pygame.draw.line(surface, color, pts[i], pts[i+1], 2)
        for p in pts:
            pygame.draw.circle(surface, (240,240,240), p, 2)

    def draw(self, target_surface, aco, top_path_colors, best_color):
        """Draw 4 stacked panels at x=0 (left column)."""
        total_h = target_surface.get_height()
        panel_h = total_h // 4

        # label height (use font metrics + padding)
        label_text_height = SMALL_FONT.get_height()
        label_h = max(20, label_text_height + 8)

        # fetch last iteration top paths
        last_paths = getattr(aco.graph, "last_iteration_paths", []) or []
        sorted_paths = sorted(last_paths, key=lambda pl: pl[1]) if last_paths else []
        top_paths = sorted_paths[:3]

        # Panel 1: Best overall
        w1 = pygame.Surface((LEFT_PANEL_WIDTH, panel_h))
        w1.fill((25, 25, 35))

        # draw label background to avoid overlap
        pygame.draw.rect(w1, (20, 20, 30), pygame.Rect(0, 0, LEFT_PANEL_WIDTH, label_h))
        if getattr(aco.graph, "best_path", None):
            self._draw_path_on_surface(w1, aco, aco.graph.best_path, best_color, top_offset=label_h)
            label = f"Best overall: {aco.graph.best_path_length:.2f}"
        else:
            label = "Best overall: -"
        # render label centered vertically in label area
        text_surf = SMALL_FONT.render(label, True, (220,220,220))
        text_y = (label_h - SMALL_FONT.get_height()) // 2
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
                self._draw_path_on_surface(wi, aco, path, color, top_offset=label_h)
                label = f"Iter top {i+1}: {length:.2f}"
            else:
                label = f"Iter top {i+1}: -"

            text_surf = SMALL_FONT.render(label, True, (220,220,220))
            text_y = (label_h - SMALL_FONT.get_height()) // 2
            wi.blit(text_surf, (8, text_y))
            target_surface.blit(wi, (0, y))

    def draw_top9(self, target_surface, aco, top_path_colors, total_width):
        # Gather paths (prefer aco.last_iteration_paths; fallback graph)
        last_paths = getattr(aco, "last_iteration_paths", None)
        if last_paths is None:
            last_paths = getattr(aco.graph, "last_iteration_paths", []) or []
        sorted_paths = sorted(last_paths, key=lambda pl: pl[1]) if last_paths else []
        top_paths = sorted_paths[:9]

        # distinct colors for 9 paths
        palette = [
            (255, 80, 80),    # red
            (255, 160, 60),   # orange
            (255, 230, 60),   # yellow
            (100, 220, 100),  # green
            (60, 180, 255),   # light blue
            (30, 90, 200),    # blue
            (170, 120, 255),  # violet
            (255, 110, 200),  # pink
            (180, 180, 180),  # gray
        ]

        cols = 3
        rows = 3
        cell_w = total_width // cols
        cell_h = SCREEN_HEIGHT // rows
        label_h = max(18, SMALL_FONT.get_height() + 6)

        for idx in range(rows * cols):
            r = idx // cols
            c = idx % cols
            x = c * cell_w
            y = r * cell_h
            panel = pygame.Surface((cell_w, cell_h))
            panel.fill((24,24,32))
            pygame.draw.rect(panel, (18,18,26), pygame.Rect(0,0,cell_w,label_h))

            if idx < len(top_paths):
                path, length = top_paths[idx]
                color = palette[idx]
                # draw path scaled to cell
                self._draw_path_on_surface(panel, aco, path, color, top_offset=label_h)
                text = f"{idx+1}. {length:.2f}"
            else:
                text = f"{idx+1}. -"

            panel.blit(
                SMALL_FONT.render(text, True, (230,230,230)),
                (6, (label_h - SMALL_FONT.get_height()) // 2)
            )
            target_surface.blit(panel, (x, y))