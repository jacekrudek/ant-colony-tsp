import os
import pygame
import pygame_gui
from pygame_gui.windows import UIFileDialog

from src.algorithm.vertice import Vertice
from src.config import CENTER_WIDTH, SCREEN_HEIGHT


class FileManager:
    def __init__(self, ui_manager, graph, on_vertices_loaded):
        self.graph = graph
        self.ui = ui_manager
        self.on_vertices_loaded = on_vertices_loaded
        self.file_dialog = None
        self._dialog_mode = None  # 'load' or 'save'

    def open_load_vertices_dialog(self):
        if self.file_dialog is not None:
            return
        self._dialog_mode = 'load'
        self.file_dialog = UIFileDialog(
            rect=pygame.Rect(100, 50, 640, 420),
            manager=self.ui,
            window_title="Load Vertices",
            allow_picking_directories=False,
            allowed_suffixes=['.csv']
        )

    # New: open a dialog to choose where to save CSV
    def open_export_vertices_dialog(self):
        if self.file_dialog is not None:
            return
        self._dialog_mode = 'save'
        self.file_dialog = UIFileDialog(
            rect=pygame.Rect(120, 70, 640, 420),
            manager=self.ui,
            window_title="Export Vertices (CSV)",
            allow_picking_directories=False,
            allowed_suffixes=['.csv']
        )

    def handle_event(self, event):
        # Path picked (OK button)
        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED and event.ui_element == self.file_dialog:
            path = event.text
            if self._dialog_mode == 'save':
                self._save_vertices_to_file(path)
            else:
                self._load_vertices_from_file(path)
            self._close_dialog()

        # Window close (X button or Cancel)
        elif event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == self.file_dialog:
            self._close_dialog()

    def _close_dialog(self):
        if self.file_dialog is not None:
            try:
                self.file_dialog.kill()
            except Exception:
                pass
            self.file_dialog = None
            self._dialog_mode = None
            print("File dialog closed")

    def is_open(self):
        return self.file_dialog is not None

    def _load_vertices_from_file(self, path: str):
        try:
            vertices = []
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Accept "x,y", "x y", or "x;y"
                    for sep in [",", ";"]:
                        line = line.replace(sep, " ")
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    x = float(parts[0])
                    y = float(parts[1])

                    # Expect coordinates in center panel space (0..CENTER_WIDTH, 0..SCREEN_HEIGHT)
                    if 0 <= x <= CENTER_WIDTH - 5 and 0 <= y <= SCREEN_HEIGHT - 5:
                        print(f"Adding vertice ({x},{y})...")
                        vertices.append(Vertice(x, y))
                    else:
                        print(f"Vertice ({x},{y}) is out of bounds, skipping...")

            if not vertices:
                print("No valid vertices in file")
                return

            g = self.graph
            g.vertices = vertices
            g.num_vertices = len(vertices)

            # Trigger a rebuild of the engine/ants via provided callback
            if callable(self.on_vertices_loaded):
                self.on_vertices_loaded(g)
            print(f"Loaded {len(vertices)} vertices from {path}")
        except Exception as e:
            print(f"Failed to load file: {e}")

    # New: direct export without dialog
    def export_vertices_to_csv(self, path: str):
        self._save_vertices_to_file(path)

    # New: internal writer used by both export and save dialog
    def _save_vertices_to_file(self, path: str):
        try:
            if not path.lower().endswith(".csv"):
                path = f"{path}.csv"

            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            verts = getattr(self.graph, "vertices", [])
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write("# x,y\n")
                for v in verts:
                    # Expect objects with x, y attributes
                    f.write(f"{float(v.x)},{float(v.y)}\n")

            print(f"Exported {len(verts)} vertices to {path}")
        except Exception as e:
            print(f"Failed to export CSV: {e}")