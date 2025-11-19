import pygame
import pygame_gui

from src.aco.problem import TSPProblem
from src.aco.colony import Colony
from src.aco.vertice import Vertice

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

            self.ui.process_events(event)

            # --- Vertex editing with mouse ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Only allow clicks inside center panel region
                if LEFT_PANEL_WIDTH <= mx <= LEFT_PANEL_WIDTH + CENTER_WIDTH and 0 <= my <= SCREEN_HEIGHT:
                    # Ensure a problem object exists
                    if getattr(self.app, "problem", None) is None:
                        self.app.problem = TSPProblem(num_vertices=0)

                    if event.button == 1:
                        # Add vertex
                        self.app.problem.vertices.append(Vertice(mx - LEFT_PANEL_WIDTH, my))
                        self._rebuild_problem_distances()
                        self._update_vertices_input()
                        self.reset_simulation()
                        print(f"Added vertex at ({mx - LEFT_PANEL_WIDTH},{my})")
                    elif event.button == 3:
                        # Remove nearest vertex (simple linear search)
                        if self.app.problem.vertices:
                            local_x = mx - LEFT_PANEL_WIDTH
                            local_y = my
                            closest_idx = None
                            closest_d2 = 25 ** 2  # threshold radius 25 px
                            for idx, v in enumerate(self.app.problem.vertices):
                                dx = v.x - local_x
                                dy = v.y - local_y
                                d2 = dx * dx + dy * dy
                                if d2 <= closest_d2:
                                    closest_d2 = d2
                                    closest_idx = idx
                            if closest_idx is not None:
                                self.app.problem.vertices.pop(closest_idx)
                                self._rebuild_problem_distances()
                                self._update_vertices_input()
                                self.reset_simulation()
                                print(f"Removed vertex #{closest_idx}")
                # Always consume mouse event when in edit mode
                continue

            # --- Sliders ---
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.sidebar.alpha_slider:
                    self.app.colony.alpha = self.sidebar.alpha_slider.get_current_value()
                elif event.ui_element == self.sidebar.beta_slider:
                    self.app.colony.beta = self.sidebar.beta_slider.get_current_value()
                elif event.ui_element == self.sidebar.evap_slider:
                    self.app.colony.evaporation_rate = self.sidebar.evap_slider.get_current_value()
                elif event.ui_element == self.sidebar.speed_slider:
                    self.app.simulation_speed = self.sidebar.speed_slider.get_current_value()

            # --- Text input finished (ants count) ---
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.sidebar.ants_input:
                    try:
                        ants = int(self.sidebar.ants_input.get_text())
                        if ants > 0:
                            self.app.colony.num_ants = ants
                            # Rebuild ants list
                            self.app.colony.ants = [self.app.colony.__class__.__bases__[0].__dict__['Ant'](self.app.colony) if False else None]  # placeholder guard
                            # Simpler: recreate colony
                            self.reset_simulation()
                            print(f"Applied ants count {ants}")
                    except Exception:
                        print("Invalid ants count")

            # --- Buttons ---
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.sidebar.apply_ants_button:
                    try:
                        ants = int(self.sidebar.ants_input.get_text())
                        if ants > 0:
                            self._recreate_colony(num_ants=ants)
                            print(f"Set ants to {ants}")
                    except Exception:
                        print("Invalid ants count")
                elif event.ui_element == self.sidebar.start_button:
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
                        stats = self.app.colony.run_iteration()
                        self.app.iteration_count += 1
                        print(f"Step {self.app.iteration_count}: best={stats['best_length']}")
                    else:
                        print("Cannot step: need at least 2 vertices")
                elif event.ui_element == self.sidebar.reset_button:
                    self.reset_simulation()
                    print("Simulation reset")
                elif event.ui_element == self.sidebar.generate_button:
                    # Generate fresh random problem using current vertex count input
                    try:
                        n = int(self.sidebar.vertices_input.get_text())
                    except Exception:
                        n = 0
                    self.app.problem = TSPProblem(num_vertices=max(0, n))
                    self._recreate_colony()
                    self._update_vertices_input()
                    print(f"Generated problem with {n} vertices")
                elif event.ui_element == self.sidebar.clear_board_button:
                    self.clear_board()

    def reset_simulation(self):
        app = self.app
        if getattr(app, "problem", None) is None:
            return
        num_ants = getattr(app.colony, "num_ants", 50)
        alpha = getattr(app.colony, "alpha", 1.0)
        beta = getattr(app.colony, "beta", 2.0)
        evaporation_rate = getattr(app.colony, "evaporation_rate", 0.1)
        app.colony = Colony(
            problem=app.problem,
            num_ants=num_ants,
            alpha=alpha,
            beta=beta,
            evaporation_rate=evaporation_rate
        )
        app.iteration_count = 0
        app.iteration_accumulator = 0.0
        if hasattr(app.colony, "last_iteration_paths"):
            app.colony.last_iteration_paths = []
        app.colony.best_path = None
        app.colony.best_path_length = float('inf')
        self._update_vertices_input()

    def clear_board(self):
        app = self.app
        try:
            old_problem = getattr(app, "problem", None)
            new_problem = TSPProblem(num_vertices=0)
            if old_problem is not None:
                if hasattr(old_problem, "width"):
                    new_problem.width = old_problem.width
                if hasattr(old_problem, "height"):
                    new_problem.height = old_problem.height
            app.problem = new_problem
        except Exception:
            try:
                if getattr(app, "problem", None) is None:
                    app.problem = TSPProblem(num_vertices=0)
                else:
                    app.problem.vertices = []
                    app.problem.num_vertices = 0
                    app.problem.distance_matrix = {}
            except Exception:
                pass
        # Recreate colony for empty problem
        self._recreate_colony()
        app.iteration_count = 0
        app.iteration_accumulator = 0.0
        try:
            if hasattr(app.colony, "last_iteration_paths"):
                app.colony.last_iteration_paths = []
            app.colony.best_path = None
            app.colony.best_path_length = float('inf')
        except Exception:
            pass
        self._update_vertices_input(force_zero=True)
        print("Cleared all vertices")

    # --- Helpers ---
    def _recreate_colony(self, num_ants=None):
        if getattr(self.app, "problem", None) is None:
            return
        if num_ants is None:
            num_ants = getattr(self.app.colony, "num_ants", 50)
        self.app.colony = Colony(
            problem=self.app.problem,
            num_ants=num_ants,
            alpha=getattr(self.app.colony, "alpha", 1.0),
            beta=getattr(self.app.colony, "beta", 2.0),
            evaporation_rate=getattr(self.app.colony, "evaporation_rate", 0.1)
        )
        self.app.iteration_count = 0
        self.app.iteration_accumulator = 0.0

    def _rebuild_problem_distances(self):
        if getattr(self.app, "problem", None) is None:
            return
        if hasattr(self.app.problem, "rebuild"):
            self.app.problem.rebuild()
        else:
            self.app.problem.num_vertices = len(self.app.problem.vertices)
            self.app.problem.distance_matrix = self.app.problem._calculate_distances()

    def _update_vertices_input(self, force_zero=False):
        try:
            if force_zero:
                self.sidebar.vertices_input.set_text("0")
            else:
                self.sidebar.vertices_input.set_text(str(len(getattr(self.app.problem, "vertices", []))))
        except Exception:
            pass

    def _can_run(self):
        p = getattr(self.app, "problem", None)
        return p is not None and p.num_vertices >= 2