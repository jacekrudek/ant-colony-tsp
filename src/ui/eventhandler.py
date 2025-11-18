import pygame
import pygame_gui
from src.aco.problem import TSPProblem
from src.aco.colony import Colony


from src.config import LEFT_PANEL_WIDTH, CENTER_WIDTH, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class EventHandler:
    def __init__(self, app):
        """
        app: instance of App — the handler will call back into app to change state.
        """
        self.app = app
        self.ui = app.ui_manager
        self.sidebar = app.sidebar

    def process(self):
        """Poll and handle all pygame events. Call from App.run() each frame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False
                continue

            # let pygame_gui handle the event first (creates UI_* events)
            self.ui.process_events(event)

            # handle mouse clicks for edit mode (only when toggle enabled)
            if event.type == pygame.MOUSEBUTTONDOWN and self.app.edit_vertices_mode:
                if self.app.simulation_running:
                    print("Stop simulation before editing vertices.")
                else:
                    mx, my = event.pos
                    cx0 = LEFT_PANEL_WIDTH if hasattr(self.app, "LEFT_PANEL_WIDTH") else LEFT_PANEL_WIDTH
                    cx0 = LEFT_PANEL_WIDTH
                    cx1 = cx0 + CENTER_WIDTH
                    if cx0 <= mx < cx1 and 0 <= my < SCREEN_HEIGHT:
                        local_x = mx - cx0
                        local_y = my
                        dst_w = self.app.main_panel.width
                        dst_h = self.app.main_panel.height
                        src_w = self.app.main_panel.src_w
                        src_h = self.app.main_panel.src_h
                        pad = self.app._center_padding
                        denom_x = max(1, (dst_w - 2 * pad))
                        denom_y = max(1, (dst_h - 2 * pad))
                        rel_x = (local_x - pad) / denom_x
                        rel_y = (local_y - pad) / denom_y
                        if 0.0 <= rel_x <= 1.0 and 0.0 <= rel_y <= 1.0:
                            px = rel_x * src_w
                            py = rel_y * src_h
                            if event.button == 1:
                                v = type("V", (), {})()
                                v.x = px
                                v.y = py
                                self.app.problem.vertices.append(v)
                                try:
                                    self.app.problem.num_vertices = len(self.app.problem.vertices)
                                except Exception:
                                    pass
                                try:
                                    self.sidebar.vertices_input.set_text(str(len(self.app.problem.vertices)))
                                except Exception:
                                    pass
                                self.reset_simulation()
                                print(f"Added vertex at ({px:.1f},{py:.1f})")
                            elif event.button == 3:
                                closest_idx = None
                                closest_dist = float("inf")
                                for idx, vv in enumerate(self.app.problem.vertices):
                                    sx, sy = self.app._map_point(vv.x, vv.y, src_w, src_h, dst_w, dst_h, padding=pad)
                                    sx += cx0
                                    dx = sx - mx
                                    dy = sy - my
                                    d2 = dx * dx + dy * dy
                                    if d2 < closest_dist:
                                        closest_dist = d2
                                        closest_idx = idx
                                if closest_idx is not None and closest_dist <= (self.app._vertex_click_threshold_px ** 2):
                                    self.app.problem.vertices.pop(closest_idx)
                                    try:
                                        self.app.problem.num_vertices = len(self.app.problem.vertices)
                                    except Exception:
                                        pass
                                    try:
                                        self.sidebar.vertices_input.set_text(str(len(self.app.problem.vertices)))
                                    except Exception:
                                        pass
                                    self.reset_simulation()
                                    print(f"Removed vertex #{closest_idx}")
                continue

            # UI events
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.sidebar.alpha_slider:
                    self.app.colony.alpha = event.value
                    self.sidebar.alpha_label.set_text(f"Alpha: {event.value:.2f}")
                elif event.ui_element == self.sidebar.beta_slider:
                    self.app.colony.beta = event.value
                    self.sidebar.beta_label.set_text(f"Beta: {event.value:.2f}")
                elif event.ui_element == self.sidebar.evap_slider:
                    self.app.colony.evaporation_rate = event.value
                    self.sidebar.evap_label.set_text(f"Evaporation: {event.value:.2f}")
                elif event.ui_element == self.sidebar.speed_slider:
                    self.app.iterations_per_second = int(event.value)
                    self.sidebar.speed_label.set_text(f"Speed: {self.app.iterations_per_second} it/s")

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.sidebar.ants_input:
                    pass

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # ants count
                if event.ui_element == self.sidebar.apply_ants_button:
                    try:
                        new_ants = int(self.sidebar.ants_input.get_text())
                        if new_ants <= 0:
                            raise ValueError("must be > 0")
                        self.app.colony = self.app.ColonyClass(  # if App reassigns class attr, else use Colony
                            problem=self.app.problem,
                            num_ants=new_ants,
                            alpha=self.app.colony.alpha,
                            beta=self.app.colony.beta,
                            evaporation_rate=self.app.colony.evaporation_rate
                        )
                        print(f"Set ants to: {new_ants}")
                    except Exception:
                        print("Invalid ants count entered")
                elif event.ui_element == self.sidebar.start_button:
                    self.app.simulation_running = True
                    print("Simulation started")
                elif event.ui_element == self.sidebar.stop_button:
                    self.app.simulation_running = False
                    print("Simulation stopped")
                elif event.ui_element == self.sidebar.step_button:
                    stats = self.app.colony.run_iteration()
                    self.app.iteration_count += 1
                    print(f"[step {self.app.iteration_count}] best={stats['best_length']:.4f} "
                          f"min={stats['min_length']:.4f} avg={stats['avg_length']:.4f} "
                          f"paths={stats['paths_count']}")
                elif event.ui_element == self.sidebar.reset_button:
                    self.reset_simulation()
                    print("Simulation reset")
                elif event.ui_element == self.sidebar.generate_button:
                    if self.app.simulation_running:
                        print("Cannot generate while simulation is running. Stop it first.")
                    else:
                        try:
                            nv = int(self.sidebar.vertices_input.get_text())
                            if nv <= 1:
                                raise ValueError("need >1 vertex")
                            self.app.problem = TSPProblem(
                                num_vertices=nv,
                                width=self.CENTER_WIDTH - 20,
                                height=self.SCREEN_HEIGHT - 20
                            )
                            self.reset_simulation()
                            print(f"Generated {nv} vertices and reset simulation.")
                        except Exception:
                            print("Invalid vertices count entered")
                elif event.ui_element == self.sidebar.edit_vertices_button:
                    if self.app.simulation_running:
                        print("Stop simulation before entering edit mode.")
                    else:
                        self.app.edit_vertices_mode = not self.app.edit_vertices_mode
                        try:
                            if self.app.edit_vertices_mode:
                                self.sidebar.edit_vertices_button.set_text("Editing: ON")
                            else:
                                self.sidebar.edit_vertices_button.set_text("Edit vertices")
                        except Exception:
                            pass
                elif event.ui_element == self.sidebar.clear_board_button:
                    if self.app.simulation_running:
                        print("Cannot clear board while simulation is running. Stop it first.")
                    else:
                        self.app.problem.vertices = []
                        try:
                            self.app.problem.num_vertices = 0
                        except Exception:
                            pass
                        try:
                            self.sidebar.vertices_input.set_text("0")
                        except Exception:
                            pass
                        self.reset_simulation()
                        print("Cleared all vertices and reset simulation.")

    def reset_simulation(self):
        """Reset colony and iteration counters while KEEPING the current problem/vertices."""
        app = self.app
        # preserve settings
        num_ants = getattr(app.colony, "num_ants", 50)
        alpha = getattr(app.colony, "alpha", 1.0)
        beta = getattr(app.colony, "beta", 2.0)
        evaporation_rate = getattr(app.colony, "evaporation_rate", 0.1)

        # recreate colony using existing problem instance so vertices remain unchanged
        app.colony = Colony(
            problem=app.problem,
            num_ants=num_ants,
            alpha=alpha,
            beta=beta,
            evaporation_rate=evaporation_rate
        )

        # reset runtime counters/state on the App
        app.iteration_count = 0
        app.iteration_accumulator = 0.0

        # clear any last-iteration visuals if present
        if hasattr(app.colony, "last_iteration_paths"):
            app.colony.last_iteration_paths = []
        app.colony.best_path = None
        app.colony.best_path_length = float('inf')

        # update sidebar UI where applicable
        try:
            app.sidebar.vertices_input.set_text(str(len(getattr(app.problem, "vertices", []))))
        except Exception:
            pass