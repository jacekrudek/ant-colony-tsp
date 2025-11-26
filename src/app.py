import pygame
import pygame_gui
from src.ui.sidebar import Sidebar
from src.ui.side_panels import SidePanels
from src.ui.main_panel import MainPanel
from src.ui.event_handler import EventHandler
from src.ui.renderer import Renderer

from src.algorithm.aco_engine import AcoEngine
from src.ui.file_manager import FileManager

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class App:
    def __init__(self):

        #pygame initializaion
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("ACO Visualisation")

        # window initialization
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # simulation controls
        self.iteration_accumulator = 0.0
        self.iteration_count = 0
        self.simulation_running = False
        self.iterations_per_second = 10

        # UI initialization
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sidebar = Sidebar(self.ui_manager)
        self.side_panels = SidePanels()
        self.main_panel = MainPanel()

        # UI logic
        self.event_handler = EventHandler(self)
        self.renderer = Renderer(self)
        self.view_mode = "standard"
        
        # algorithm
        self.aco_engine = AcoEngine(
            alpha=1.0,
            beta=1.0,
            evaporation_rate=0.1,
            num_vertices = 20,
            num_ants = 50
        )

        # file manager
        self.file_manager = FileManager(
            ui_manager=self.ui_manager, 
            graph=self.aco_engine.graph,
            on_vertices_loaded=self.event_handler.reset_simulation
        )



    def run(self):
        """main loop"""
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
                stats = self.aco_engine.run_iteration()
                self.iteration_accumulator -= interval
                self.iteration_count += 1
        self.ui_manager.update(time_delta)