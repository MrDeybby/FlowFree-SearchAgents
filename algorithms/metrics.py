import os
import time
import tracemalloc
from abc import abstractmethod

from game.base_player import Player
from game.flow_free import FlowFreeBoard, Connection

class Metrics(Player):
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        
        # Métricas de ren~dimiento
        self.start_time = None
        self.total_nodes_expanded = 0
        self.max_search_depth_overall = 0

    @abstractmethod
    def play(self, board: FlowFreeBoard, level_name: str):
        pass

    def _generate_reports(self, final_board: FlowFreeBoard, level_name: str):
        """Crea los archivos de salida .txt y .csv con las métricas de rendimiento."""
        running_time = time.monotonic() - self.start_time
        _, max_ram_usage = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        max_ram_usage /= 1024**2  # Convertir a MB

        cost_of_path = sum(len(conn.road) - 1 for conn in final_board.connections)
        search_depth = cost_of_path  # La profundidad de la solución es el total de celdas del camino

        path_to_goal_matrix = [['' for _ in range(final_board.columns)] for _ in range(final_board.rows)]
        for conn in final_board.connections:
            # Encuentra la letra inicial del color
            char = next((key for key, value in Connection.NAMES.items() if value == conn.name), '?')
            for (px, py) in conn.road:
                path_to_goal_matrix[py][px] = char

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # A TXT
        file_base_name = f"{self.name}_{level_name.replace('.txt', '')}"
        txt_filename = os.path.join(output_dir, f"{file_base_name}.txt")
        with open(txt_filename, 'w') as f:
            f.write(f"path_to_goal: {path_to_goal_matrix}\n")
            f.write(f"cost_of_path: {cost_of_path}\n")
            f.write(f"nodes_expanded: {self.total_nodes_expanded}\n")
            f.write(f"search_depth: {search_depth}\n")
            f.write(f"max_search_depth: {self.max_search_depth_overall}\n")
            f.write(f"running_time: {running_time:.8f}\n")
            f.write(f"max_ram_usage: {max_ram_usage:.8f}\n")
        print(f"\nReporte .txt guardado en: {txt_filename}")