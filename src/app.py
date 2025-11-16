import pygame
import pygame_gui
from src.ui.sidebar import Sidebar
from src.ui.sidepanels import SidePanels
from src.ui.mainpanel import MainPanel

from src.aco.problem import TSPProblem
from src.aco.colony import Colony

# Layout constants
LEFT_PANEL_WIDTH = 200
CENTER_WIDTH = 800
SIDEBAR_WIDTH = 200
SCREEN_WIDTH = LEFT_PANEL_WIDTH + CENTER_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = 600

# colours
TOP_PATH_COLORS = [(255, 100, 100), (255, 180, 80), (80, 180, 255)]
BEST_COLOR = (0, 255, 0)
PURPLE = (150, 80, 200)

class App:
    def __init__(self):

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("ACO Visualisation")

        # Create the main window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.small_font = pygame.font.SysFont(None, 16)

        # UI manager and sidebar (sidebar placed to the right of center)
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sidebar expects the x offset for layout; give it left + center width
        self.sidebar = Sidebar(LEFT_PANEL_WIDTH + CENTER_WIDTH, SIDEBAR_WIDTH, SCREEN_HEIGHT, self.ui_manager)

        # --- Problem & Colony --
        # vertices were generated previously to fit GAME_WIDTH x SCREEN_HEIGHT;
        # now center area is CENTER_WIDTH so pass its inner drawing size
        self.problem = TSPProblem(
            num_vertices=20,
            width=CENTER_WIDTH - 20,
            height=SCREEN_HEIGHT - 20
        )
        self.colony = Colony(
            problem=self.problem,
            num_ants=50,
            alpha=1.0,
            beta=2.0,
            evaporation_rate=0.1
        )
        self.side_panels = SidePanels(
            panel_width=LEFT_PANEL_WIDTH,
            panel_height=SCREEN_HEIGHT,
            small_font=self.small_font,
            src_w=CENTER_WIDTH - 20,
            src_h=SCREEN_HEIGHT - 20
        )
        self.main_panel = MainPanel(
            width= CENTER_WIDTH, 
            height= SCREEN_HEIGHT, 
            src_w=CENTER_WIDTH - 20, 
            src_h=SCREEN_HEIGHT - 20,
            purple=PURPLE, 
            best_color=BEST_COLOR
        )


        # simulation controls
        self.simulation_running = False
        self.iterations_per_second = 10
        self.iteration_accumulator = 0.0
        self.iteration_count = 0

    def run(self):
        """The main game loop."""
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0  # seconds
            self.handle_events()
            self.update(time_delta)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.sidebar.alpha_slider:
                    self.colony.alpha = event.value
                    self.sidebar.alpha_label.set_text(f"Alpha: {event.value:.2f}")
                elif event.ui_element == self.sidebar.beta_slider:
                    self.colony.beta = event.value
                    self.sidebar.beta_label.set_text(f"Beta: {event.value:.2f}")
                elif event.ui_element == self.sidebar.evap_slider:
                    self.colony.evaporation_rate = event.value
                    self.sidebar.evap_label.set_text(f"Evaporation: {event.value:.2f}")
                elif event.ui_element == self.sidebar.speed_slider:
                    self.iterations_per_second = int(event.value)
                    self.sidebar.speed_label.set_text(f"Speed: {self.iterations_per_second} it/s")

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.sidebar.ants_input:
                    pass

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.sidebar.apply_ants_button:
                    try:
                        new_ants = int(self.sidebar.ants_input.get_text())
                        if new_ants <= 0:
                            raise ValueError("must be > 0")
                        self.colony = Colony(
                            problem=self.problem,
                            num_ants=new_ants,
                            alpha=self.colony.alpha,
                            beta=self.colony.beta,
                            evaporation_rate=self.colony.evaporation_rate
                        )
                        print(f"Set ants to: {new_ants}")
                    except ValueError:
                        print("Invalid ants count entered")
                elif event.ui_element == self.sidebar.start_button:
                    self.simulation_running = True
                    print("Simulation started")
                elif event.ui_element == self.sidebar.stop_button:
                    self.simulation_running = False
                    print("Simulation stopped")
                elif event.ui_element == self.sidebar.step_button:
                    # run exactly one iteration and log stats (does not toggle running)
                    stats = self.colony.run_iteration()
                    self.iteration_count += 1
                    print(f"[step {self.iteration_count}] best={stats['best_length']:.4f} "
                          f"min={stats['min_length']:.4f} avg={stats['avg_length']:.4f} "
                          f"paths={stats['paths_count']}")

    def update(self, time_delta):
        if self.simulation_running:
            self.iteration_accumulator += time_delta
            interval = 1.0 / max(1, self.iterations_per_second)
            while self.iteration_accumulator >= interval:
                stats = self.colony.run_iteration()
                self.iteration_accumulator -= interval
                self.iteration_count += 1
                print(f"[iter {self.iteration_count}] best={stats['best_length']:.4f} "
                      f"min={stats['min_length']:.4f} avg={stats['avg_length']:.4f} "
                      f"paths={stats['paths_count']}")
        self.ui_manager.update(time_delta)

    # utility: map problem-space point -> target rect with padding
    def _map_point(self, x, y, src_w, src_h, dst_w, dst_h, padding=8):
        sx = padding + (x / max(1, src_w)) * (dst_w - 2 * padding)
        sy = padding + (y / max(1, src_h)) * (dst_h - 2 * padding)
        return int(sx), int(sy)

    def _draw_path_on_surface(self, surface, path, color, src_w, src_h):
        if not path or len(path) < 2:
            return
        pts = []
        dst_w, dst_h = surface.get_size()
        for vidx in path:
            v = self.problem.vertices[vidx]
            pts.append(self._map_point(v.x, v.y, src_w, src_h, dst_w, dst_h))
        # draw segments
        for i in range(len(pts) - 1):
            pygame.draw.line(surface, color, pts[i], pts[i+1], 2)
        # draw nodes
        for p in pts:
            pygame.draw.circle(surface, (240,240,240), p, 2)

    def draw(self):
        # Fill background
        self.screen.fill((10, 10, 10))

        self.side_panels.draw(self.screen, self.problem, self.colony, TOP_PATH_COLORS, BEST_COLOR)

        self.main_panel.draw(self.screen, LEFT_PANEL_WIDTH, self.problem, self.colony)

         # --- iteration counter (top of center area) ---
        iter_text = f"Iteration: {self.iteration_count}"
        iter_surf = self.small_font.render(iter_text, True, (220, 220, 220))
        iter_pos = (LEFT_PANEL_WIDTH + 8, 8)  # adjust position if you want
        self.screen.blit(iter_surf, iter_pos)

        # ===== Sidebar (right) background and UI =====
        sidebar_bg = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))
        sidebar_bg.fill((50,50,50))
        self.screen.blit(sidebar_bg, (LEFT_PANEL_WIDTH + CENTER_WIDTH, 0))

        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()