# in src/ui/sidebar.py
import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UIHorizontalSlider, UITextEntryLine, UIButton

from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_PATH_COLORS, BEST_COLOR, PURPLE

class Sidebar:
    """
    Manages the UI sidebar on the right side of the screen.
    """
    def __init__(self, ui_manager):
        alpha = 1.0
        beta = 1.0
        evap = 0.1
        ants = 50
        speed = 10

        x = LEFT_PANEL_WIDTH + CENTER_WIDTH + 10
        y = 10
        w = SIDEBAR_WIDTH - 20
        spacing = 8
        label_h = 24
        slider_h = 20
        input_h = 28
        btn_h = 28

        # Title
        self.title = UILabel(pygame.Rect(x, y, w, label_h),
                             text="Algorithm Parameters",
                             manager=ui_manager)
        y += label_h + spacing

        # --- New: number of vertices + Generate button ---
        self.vertices_label = UILabel(pygame.Rect(x, y, w, label_h),
                                      text="Vertices:",
                                      manager=ui_manager)
        y += label_h + 4
        self.vertices_input = UITextEntryLine(pygame.Rect(x, y, w, input_h), manager=ui_manager)
        # set initial if provided
        self.vertices_input.set_text("20")
        y += input_h + spacing

        self.generate_button = UIButton(pygame.Rect(x, y, w, btn_h),
                                        text="Generate",
                                        manager=ui_manager)
        y += btn_h + spacing

        # Clear board button
        self.clear_board_button = UIButton(pygame.Rect(x, y, w, btn_h),
                                           text="Clear board",
                                           manager=ui_manager)
        y += btn_h + spacing

        # Speed (iterations per second)
        self.speed_label = UILabel(pygame.Rect(x, y, w, label_h),
                                   text=f"Speed: {speed} it/s",
                                   manager=ui_manager)
        y += label_h + 4
        self.speed_slider = UIHorizontalSlider(pygame.Rect(x, y, w, slider_h),
                                               start_value=speed,
                                               value_range=(1, 60),
                                               manager=ui_manager)
        y += slider_h + spacing

        # Alpha
        self.alpha_label = UILabel(pygame.Rect(x, y, w, label_h),
                                   text=f"Alpha: {alpha:.2f}",
                                   manager=ui_manager)
        y += label_h + 4
        self.alpha_slider = UIHorizontalSlider(pygame.Rect(x, y, w, slider_h),
                                               start_value=alpha,
                                               value_range=(0.0, 5.0),
                                               manager=ui_manager)
        y += slider_h + spacing

        # Beta
        self.beta_label = UILabel(pygame.Rect(x, y, w, label_h),
                                  text=f"Beta: {beta:.2f}",
                                  manager=ui_manager)
        y += label_h + 4
        self.beta_slider = UIHorizontalSlider(pygame.Rect(x, y, w, slider_h),
                                              start_value=beta,
                                              value_range=(0.0, 10.0),
                                              manager=ui_manager)
        y += slider_h + spacing

        # Evaporation
        self.evap_label = UILabel(pygame.Rect(x, y, w, label_h),
                                   text=f"Evaporation: {evap:.2f}",
                                   manager=ui_manager)
        y += label_h + 4
        self.evap_slider = UIHorizontalSlider(pygame.Rect(x, y, w, slider_h),
                                              start_value=evap,
                                              value_range=(0.0, 1.0),
                                              manager=ui_manager)
        y += slider_h + spacing

        # Number of ants input + button
        self.ants_label = UILabel(pygame.Rect(x, y, w, label_h),
                                  text="Number of ants:",
                                  manager=ui_manager)
        y += label_h + 4
        self.ants_input = UITextEntryLine(pygame.Rect(x, y, w, input_h), manager=ui_manager)
        self.ants_input.set_text(str(ants))
        
        y += input_h + spacing

        # Start / Stop buttons
        # Start visualisation
        self.start_button = UIButton(pygame.Rect(x, y, (w // 2) - 4, btn_h),
                                     text="Start",
                                     manager=ui_manager)
        # Stop visualisation
        self.stop_button = UIButton(pygame.Rect(x + (w // 2) + 4, y, (w // 2) - 4, btn_h),
                                    text="Stop",
                                    manager=ui_manager)
        
        y += btn_h + spacing

        # Step (single-iteration) button
        self.step_button = UIButton(pygame.Rect(x, y, w, btn_h),
                                    text="Step",
                                    manager=ui_manager)
        
        y += btn_h + spacing

        # Reset button
        self.reset_button = UIButton(pygame.Rect(x, y, w, btn_h),
                                    text="Reset",
                                    manager=ui_manager)
        
        y += btn_h + spacing

        self.view_toggle_button = UIButton(pygame.Rect(x, y, w, btn_h),
                                    text="View: Standard",
                                    manager=ui_manager)