# in src/app.py

import pygame
import pygame_gui
from src.ui.sidebar import Sidebar

# --- 1. Add new imports ---
from src.aco.problem import TSPProblem
from src.aco.colony import Colony
import time

# --- Constants ---
GAME_WIDTH = 800
SIDEBAR_WIDTH = 200
SCREEN_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = 600

class App:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("My Pygame App")

        # Create the main window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # ... existing pygame, screen, clock setup ...
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sidebar = Sidebar(GAME_WIDTH, SIDEBAR_WIDTH, SCREEN_HEIGHT, self.ui_manager)

        # --- Game-specific variables ---
        self.slider_value = 50.0 # To store the slider's value

        # --- 2. Initialize the ACO Problem ---
        self.problem = TSPProblem(
            num_vertices=20, 
            width=GAME_WIDTH - 20,  # Give a 10px margin for drawing
            height=SCREEN_HEIGHT - 20
        )
        self.colony = Colony(
            problem=self.problem,
            num_ants=50,
            alpha=1.0,  # Pheromone importance
            beta=2.0,   # Distance importance
            evaporation_rate=0.1
        )

        self.simulation_running = False

        self.iterations_per_second = 10  # default
        self.iteration_accumulator = 0.0
        self.iteration_count = 0
        self.last_log_time = time.time()
        # ...

    def run(self):
        """The main game loop."""
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0  # Time since last frame in seconds

            # 1. Handle Events
            self.handle_events()

            # 2. Update Logic
            self.update(time_delta)

            # 3. Draw Everything
            self.draw()

        pygame.quit()

    def handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            self.ui_manager.process_events(event)

            # --- 3. Connect UI to Colony Params ---
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.sidebar.alpha_slider:
                    self.colony.alpha = event.value
                    # update label text
                    self.sidebar.alpha_label.set_text(f"Alpha: {event.value:.2f}")
                elif event.ui_element == self.sidebar.beta_slider:
                    self.colony.beta = event.value
                    self.sidebar.beta_label.set_text(f"Beta: {event.value:.2f}")
                elif event.ui_element == self.sidebar.evap_slider:
                    self.colony.evaporation_rate = event.value
                    self.sidebar.evap_label.set_text(f"Evaporation: {event.value:.2f}")
                elif event.ui_element == self.sidebar.speed_slider:
                    # update iterations per second
                    self.iterations_per_second = int(event.value)
                    self.sidebar.speed_label.set_text(f"Speed: {self.iterations_per_second} it/s")


            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                # keep but we don't need to do anything special here
                if event.ui_element == self.sidebar.ants_input:
                    pass

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.sidebar.apply_ants_button:
                    # Try to parse ants count and recreate colony with new size
                    try:
                        new_ants = int(self.sidebar.ants_input.get_text())
                        if new_ants <= 0:
                            raise ValueError("must be > 0")
                        # Recreate colony so pheromone matrix and ants list reset to new num
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

    def update(self, time_delta):
        """Update game state and UI."""
        
        # Run iterations at the requested rate
        if self.simulation_running:
            self.iteration_accumulator += time_delta
            interval = 1.0 / max(1, self.iterations_per_second)
            # run as many iterations as fit into the accumulator
            while self.iteration_accumulator >= interval:
                stats = self.colony.run_iteration()
                self.iteration_accumulator -= interval
                self.iteration_count += 1

                # Log iteration stats to console
                print(f"[iter {self.iteration_count}] best={stats['best_length']:.4f} "
                      f"min={stats['min_length']:.4f} avg={stats['avg_length']:.4f} "
                      f"paths={stats['paths_count']}")
        
        self.ui_manager.update(time_delta)

    def draw(self):
        """Draw everything to the screen."""
        
        # 1. Draw the "Game" area (left side)
        game_surface = pygame.Surface((GAME_WIDTH, SCREEN_HEIGHT))
        game_surface.fill(pygame.Color(0, 0, 20)) # Very dark blue
        
        # --- 5. Draw the ACO Visualization ---
        
        # A. Draw Pheromone Trails (optional and can be slow)
        # We find a max pheromone to normalize for brightness
        max_pheromone = max(max(row.values()) for row in self.colony.pheromone_matrix.values() if row)
        if max_pheromone == 0: max_pheromone = 1.0 # Avoid division by zero

        for i in range(self.problem.num_vertices):
            for j in range(i + 1, self.problem.num_vertices):
                vertice_a = self.problem.vertices[i]
                vertice_b = self.problem.vertices[j]
                
                pheromone = self.colony.pheromone_matrix[i][j]
                # Normalize to a 0-255 alpha (transparency) value
                alpha = min(255, int((pheromone / max_pheromone) * 255))
                
                if alpha > 10: # Only draw trails with some pheromone
                    # Add 10 to x/y for the margin we created
                    pygame.draw.line(game_surface, (100, 100, 255, alpha), 
                                     (vertice_a.x + 10, vertice_a.y + 10), 
                                     (vertice_b.x + 10, vertice_b.y + 10), 1)

        # B. Draw the Best Path
        if self.colony.best_path:
            path_points = []
            for vertice_index in self.colony.best_path:
                vertice = self.problem.vertices[vertice_index]
                path_points.append((vertice.x + 10, vertice.y + 10))
            pygame.draw.lines(game_surface, (0, 255, 0), False, path_points, 2) # Bright green
            
        # C. Draw Vertices
        for vertice in self.problem.vertices:
            pygame.draw.circle(game_surface, (255, 255, 255), 
                               (vertice.x + 10, vertice.y + 10), 5) # White circles

        # --- Blit game surface and UI (existing code) ---
        self.screen.blit(game_surface, (0, 0))

        # Draw the sidebar background
        sidebar_bg = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))
        sidebar_bg.fill(pygame.Color(50, 50, 50)) # Dark grey
        self.screen.blit(sidebar_bg, (GAME_WIDTH, 0))

        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()