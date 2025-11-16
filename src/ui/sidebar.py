# in src/ui/sidebar.py
import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UIHorizontalSlider, UITextEntryLine, UIButton

class Sidebar:
    """
    Manages the UI sidebar on the right side of the screen.
    """
    def __init__(self, game_width, sidebar_width, screen_height, ui_manager, initial_params=None):
        ip = initial_params or {}
        alpha = float(ip.get("alpha", 1.0))
        beta = float(ip.get("beta", 2.0))
        evap = float(ip.get("evaporation_rate", 0.1))
        ants = int(ip.get("num_ants", 50))
        speed = int(ip.get("speed", 10)) 

        x = game_width + 10
        y = 10
        w = sidebar_width - 20
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

        self.apply_ants_button = UIButton(pygame.Rect(x, y, w, btn_h),
                                          text="Apply ants count",
                                          manager=ui_manager)
        
        y += btn_h + spacing

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