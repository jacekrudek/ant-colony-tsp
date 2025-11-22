import pygame

from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_PATH_COLORS, BEST_COLOR, SMALL_FONT


class Renderer:
    def __init__(self, app):
        """
        app: instance of App — renderer will read state from app and draw onto app.screen.
        """
        self.app = app
    
    def draw(self):
        app = self.app
        screen = app.screen

        # Fill background
        screen.fill((10, 10, 10))

        # LEFT panels
        app.side_panels.draw(screen, app.aco_engine, TOP_PATH_COLORS if hasattr(app, "TOP_PATH_COLORS") else TOP_PATH_COLORS, BEST_COLOR if hasattr(app, "BEST_COLOR") else BEST_COLOR)

        # CENTER panel
        app.main_panel.draw(screen, LEFT_PANEL_WIDTH, app.aco_engine)

        # iteration counter (top of center area)
        iter_text = f"Iteration: {app.iteration_count}"
        iter_surf = SMALL_FONT.render(iter_text, True, (220, 220, 220))
        iter_pos = (LEFT_PANEL_WIDTH + 8, 8)
        screen.blit(iter_surf, iter_pos)

        # Sidebar background (right)
        sidebar_bg = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))
        sidebar_bg.fill((50,50,50))
        screen.blit(sidebar_bg, (LEFT_PANEL_WIDTH + CENTER_WIDTH, 0))

        # draw UI (pygame_gui)
        app.ui_manager.draw_ui(screen)

        # flip display
        pygame.display.flip()