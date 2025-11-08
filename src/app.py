import pygame
import pygame_gui
from src.ui.sidebar import Sidebar

# UI variables
GAME_WIDTH = 800
SIDEBAR_WIDTH = 200
SCREEN_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = 600

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ACO Algorithm Visualisation")

        # setup app window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        #setup ui_manager
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        #add sidebar
        self.sidebar = Sidebar(GAME_WIDTH, SIDEBAR_WIDTH, SCREEN_HEIGHT, self.ui_manager)

        #setup sidebar properties
        self.slider_value = 50.0 

    def run(self):
        # main app loop
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
        # process inputs 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Pass events to the UI Manager
            self.ui_manager.process_events(event)

            # --- Handle specific UI events ---
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.sidebar.my_slider:
                    self.slider_value = event.value
                    print(f"Slider moved to: {self.slider_value}")

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.sidebar.my_input_box:
                    print(f"Text entered: {event.text}")

    def update(self, time_delta):
        """Update game state and UI."""
        self.ui_manager.update(time_delta)

    def draw(self):
        """Draw everything to the screen."""
        
        # 1. Draw the "Game" area (left side)
        game_surface = pygame.Surface((GAME_WIDTH, SCREEN_HEIGHT))
        game_surface.fill(pygame.Color(0, 0, 50)) # Dark blue
        
        # Example: Draw a circle whose size is controlled by the slider
        radius = int(self.slider_value)
        pygame.draw.circle(game_surface, (255, 255, 255), (GAME_WIDTH // 2, SCREEN_HEIGHT // 2), radius)

        self.screen.blit(game_surface, (0, 0))

        # 2. Draw the sidebar background (right side)
        sidebar_bg = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))
        sidebar_bg.fill(pygame.Color(50, 50, 50)) # Dark grey
        self.screen.blit(sidebar_bg, (GAME_WIDTH, 0))

        # 3. Draw the UI elements (pygame-gui handles this)
        self.ui_manager.draw_ui(self.screen)

        # 4. Update the display
        pygame.display.flip()