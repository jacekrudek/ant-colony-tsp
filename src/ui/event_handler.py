import pygame
import pygame_gui

from src.map.vertice import Vertice
from src.algorithm.aco_engine import AcoEngine

from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT


class EventHandler:
    def __init__(self, app):
        self.app = app
        self.ui = app.ui_manager
        self.sidebar = app.sidebar

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False
                continue

            if self.app.file_manager:
                self.app.file_manager.handle_event(event)

            self.ui.process_events(event)

            # Vertex editing with mouse 
            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.app.file_manager and self.app.file_manager.is_open():
                    continue

                mx, my = event.pos

                if LEFT_PANEL_WIDTH <= mx <= LEFT_PANEL_WIDTH + CENTER_WIDTH and 0 <= my <= SCREEN_HEIGHT:

                    if event.button == 1:

                        self.app.aco_engine.graph.vertices.append(Vertice(mx - LEFT_PANEL_WIDTH, my))

                        self.app.aco_engine.graph.num_vertices += 1


                        self.reset_simulation(self.app.aco_engine.graph)

                        print(f"Added vertex at ({mx - LEFT_PANEL_WIDTH},{my})")

            # Sliders
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.sidebar.alpha_slider:
                    val = event.value
                    self.app.aco_engine.alpha = val
                    self.sidebar.alpha_label.set_text(f"Alpha: {val:.2f}")
                elif event.ui_element == self.sidebar.beta_slider:
                    val = event.value
                    self.app.aco_engine.beta = val
                    self.sidebar.beta_label.set_text(f"Beta: {val:.2f}")
                elif event.ui_element == self.sidebar.evap_slider:
                    val = event.value
                    self.app.aco_engine.evaporation_rate = val
                    self.sidebar.evap_label.set_text(f"Evaporation: {val:.2f}")
                elif event.ui_element == self.sidebar.speed_slider:
                    val = event.value
                    self.app.iterations_per_second = val
                    self.sidebar.speed_label.set_text(f"Speed: {val} it/s")

            # Text input finished
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.sidebar.ants_input:
                    try:
                        ants = int(self.sidebar.ants_input.get_text())
                        if ants > 0 and ants <= 100:
                            self.app.aco_engine.num_ants = ants
                            # Rebuild ants list
                            self.reset_simulation(self.app.aco_engine.graph)
                            print(f"Applied ants count {ants}")
                        else:
                            self.sidebar.ants_input.set_text(str(self.app.aco_engine.num_ants))
                            print("Invalid ants count - outside range")
                    except Exception:
                        self.sidebar.ants_input.set_text(str(self.app.aco_engine.num_ants))
                        print("Invalid ants count")
                elif event.ui_element == self.sidebar.vertices_input:
                    try:
                        vertices = int(self.sidebar.vertices_input.get_text())
                        if vertices > 0 and vertices <= 150:
                            self.app.aco_engine.graph.num_vertices = vertices
                            # Rebuild ants list
                            self.reset_simulation()
                            print(f"Applied vertice count {vertices}")
                        else:
                            self.sidebar.vertices_input.set_text(str(self.app.aco_engine.graph.num_vertices))
                            print("Invalid vertice count - outside range")
                    except Exception:
                        self.sidebar.vertices_input.set_text(str(self.app.aco_engine.graph.num_vertices))
                        print("Invalid vertice count")


            # Buttons
            if event.type == pygame_gui.UI_BUTTON_PRESSED: 
                if event.ui_element == self.sidebar.start_button:
                    if self._can_run():
                        self.app.simulation_running = True
                        print("Simulation started")
                    else:
                        print("Cannot start: need at least 2 vertices")
                elif event.ui_element == self.sidebar.stop_button:
                    self.app.simulation_running = False
                    print("Simulation stopped")
                elif event.ui_element == self.sidebar.step_button:
                    if self._can_run():
                        stats = self.app.aco_engine.run_iteration()
                        self.app.iteration_count += 1
                    else:
                        print("Cannot step: need at least 2 vertices")
                elif event.ui_element == self.sidebar.reset_button:
                    self.reset_simulation(self.app.aco_engine.graph)
                    print("Simulation reset")
                elif event.ui_element == self.sidebar.generate_button:
                    self.reset_simulation()
                    print(f"Generated problem with vertices")
                elif event.ui_element == self.sidebar.clear_board_button:
                    self.app.aco_engine.graph.num_vertices = 0
                    self.reset_simulation()
                elif event.ui_element == self.sidebar.view_toggle_button:
                    if self.app.view_mode == "standard":
                        self.app.view_mode = "top9"
                        self.sidebar.view_toggle_button.set_text("View: Top 9")
                    else:
                        self.app.view_mode = "standard"
                        self.sidebar.view_toggle_button.set_text("View: Standard")
                elif event.ui_element == self.sidebar.load_vertice_button:
                    self.app.file_manager.open_load_vertices_dialog()
                elif event.ui_element == self.sidebar.export_vertice_button:
                    self.app.file_manager.open_export_vertices_dialog()

    def reset_simulation(self, graph = None):


        num_ants = getattr(self.app.aco_engine, "num_ants", 50)
        alpha = getattr(self.app.aco_engine, "alpha", 1.0)
        beta = getattr(self.app.aco_engine, "beta", 2.0)
        evaporation_rate = getattr(self.app.aco_engine, "evaporation_rate", 0.1)
        num_vertices = getattr(self.app.aco_engine.graph, "num_vertices", 10)


        if graph is None:
            self.app.aco_engine = AcoEngine(
                alpha=alpha,
                beta=beta,
                evaporation_rate=evaporation_rate,
                num_vertices = num_vertices,
                num_ants = num_ants
            )
        else:
            self.app.aco_engine = AcoEngine(
                alpha=alpha,
                beta=beta,
                evaporation_rate=evaporation_rate,
                num_vertices = num_vertices,
                num_ants = num_ants,
                graph=graph
            )

        self.app.file_manager.graph = self.app.aco_engine.graph

        self.app.iteration_count = 0
        self.app.iteration_accumulator = 0.0
        
        self.sidebar.vertices_input.set_text(str(self.app.aco_engine.graph.num_vertices))

    
    def _can_run(self):
        if self.app.aco_engine.graph.num_vertices >= 2:
            return True
        
        return False