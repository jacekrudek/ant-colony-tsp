import pygame
import pygame_gui
from src.ui.sidebar import Sidebar
from src.ui.sidepanels import SidePanels
from src.ui.mainpanel import MainPanel
from src.ui.eventhandler import EventHandler
from src.ui.renderer import Renderer

from src.aco.problem import TSPProblem
from src.aco.colony import Colony

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

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
        self.sidebar = Sidebar(self.ui_manager)

        self.problem = TSPProblem(num_vertices=20)
        self.colony = Colony(
            problem=self.problem,
            num_ants=50,
            alpha=1.0,
            beta=2.0,
            evaporation_rate=0.1
        )
        self.side_panels = SidePanels(small_font=self.small_font)
        self.main_panel = MainPanel()

        self.event_handler = EventHandler(self)

        self.renderer = Renderer(self)

        # simulation controls
        self.iteration_accumulator = 0.0
        self.iteration_count = 0
        self.simulation_running = False
        self.iterations_per_second = 10


    def run(self):
        """The main game loop."""
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0  # seconds
            self.event_handler.process()
            self.update(time_delta)
            self.renderer.draw()
        pygame.quit()

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