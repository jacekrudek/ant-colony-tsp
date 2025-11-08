# in src/ui/sidebar.py
import pygame
import pygame_gui

class Sidebar:
    """
    Manages the UI sidebar on the right side of the screen.
    """
    def __init__(self, x_pos, width, height, manager):
        self.manager = manager
        self.width = width
        self.height = height
        self.x_pos = x_pos

        # This rectangle defines the bounds of the sidebar
        self.rect = pygame.Rect(x_pos, 0, width, height)

        # 2. Create a Slider
        # Note: We position it relative to the sidebar's left edge (x_pos)
        self.my_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((x_pos + 20), 60, width - 40, 20),
            start_value=50,
            value_range=(0, 100),
            manager=self.manager
        )

        # 3. Create an Input Box (Text Entry)
        self.my_input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((x_pos + 20), 100, width - 40, 30),
            manager=self.manager
        )
        self.my_input_box.set_text("Hello...")