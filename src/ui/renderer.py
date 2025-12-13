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
        screen.fill((10, 10, 10))

        # sidebar background (right column always)
        sidebar_x = LEFT_PANEL_WIDTH + CENTER_WIDTH
        sidebar_bg = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))
        sidebar_bg.fill((50,50,50))
        screen.blit(sidebar_bg, (sidebar_x, 0))

        if getattr(app, "view_mode", "standard") == "top9":
            # Use combined width of previous side + main area
            full_width = LEFT_PANEL_WIDTH + CENTER_WIDTH
            app.side_panels.draw_top9(screen, app.aco_engine, TOP_PATH_COLORS, full_width)
        else:
            app.side_panels.draw(screen, app.aco_engine, TOP_PATH_COLORS, BEST_COLOR)
            app.main_panel.draw(screen, LEFT_PANEL_WIDTH, app.aco_engine)

        iter_text = f"Iteration: {app.iteration_count}"
        iter_surf = SMALL_FONT.render(iter_text, True, (220, 220, 220))
        screen.blit(iter_surf, (LEFT_PANEL_WIDTH + CENTER_WIDTH - 80, 8))

        app.ui_manager.draw_ui(screen)
        pygame.display.flip()
        pygame.display.flip()