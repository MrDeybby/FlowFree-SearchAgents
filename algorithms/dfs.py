# Importaciones necesarias
import time
import copy
import os
import csv
import tracemalloc
import random

# Importaciones de los módulos de tu proyecto
from game.player import Player
from game.flow_free import FlowFreeBoard, Connection

class DFSPlayer(Player):
    """
    Agente que resuelve Flow Free usando una estrategia de DFS local y reinicio.
    Ahora incluye la medición de rendimiento y generación de reportes.
    """

    def __init__(self):
        """Inicializa el agente, la memoria y las variables para las métricas."""
        super().__init__()
        self.failed_states = set()
        self.name = "DFS"
    

        # SECCIÓN DE MÉTRICAS
        self.start_time = None
        self.total_nodes_expanded = 0
        self.max_search_depth_overall = 0
        
    def _get_hashable_state(self, board: FlowFreeBoard):
        """Crea una representación inmutable del estado del tablero."""
        return tuple(map(tuple, board.get_state()))

    def _dfs_for_one_color(self, board: FlowFreeBoard, target_connection: Connection):
        """
        Busca un camino para UNA SOLA conexión usando DFS.
        MODIFICADO: Ahora también devuelve métricas de su búsqueda local.
        """
        start_point = target_connection.points[0]
        end_point = target_connection.points[1]

        frontier = [(start_point, [start_point])]
        visited = {start_point}
        
        # --- MÉTRICAS LOCALES ---
        nodes_expanded_this_run = 0
        max_depth_this_run = 0

        occupied_by_others = set()
        for conn in board.connections:
            if conn != target_connection:
                occupied_by_others.update(conn.road)
                occupied_by_others.update(conn.points)

        while frontier:
            current_point, path = frontier.pop()
            nodes_expanded_this_run += 1
            max_depth_this_run = max(max_depth_this_run, len(path))

            if current_point == end_point:
                return path, nodes_expanded_this_run, max_depth_this_run

            (x, y) = current_point
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            random.shuffle(neighbors)

            for neighbor in neighbors:
                if neighbor not in visited:
                    if not board._validate_cell(neighbor[0], neighbor[1]):
                        continue
                    if neighbor in occupied_by_others:
                        continue
                    
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    frontier.append((neighbor, new_path))
        
        return None, nodes_expanded_this_run, max_depth_this_run

    def play(self, board: FlowFreeBoard, level_name: str = "unknown_level"):
        """
        Método principal que orquesta la estrategia de resolución.
        MODIFICADO: Ahora maneja el inicio/fin de la medición y llama a la generación de reportes.
        """
        # MANEJO DE MÉTRICAS GLOBALES (INICIO)
        if self.start_time is None:
            self.start_time = time.monotonic()
            tracemalloc.start()

        all_completed = all(conn.is_completed for conn in board.connections)

        if all_completed and board.percentage_filled() < 100:
            board_state = self._get_hashable_state(board)
            self.failed_states.add(board_state)
            print(f"DFS Player: Callejón sin salida. Reiniciando. Memoria: {len(self.failed_states)}")
            for conn in board.connections:
                conn.clean_road()
            return board.connections[0].points[0]

        if all_completed and board.percentage_filled() == 100:
            print("DFS Player: ¡Solución encontrada!")
            # --- MANEJO DE MÉTRICAS GLOBALES (FIN) ---
            self._generate_reports(board, level_name)
            return None 

        incomplete_connections = [conn for conn in board.connections if not conn.is_completed]
        
        untouched_connections = [conn for conn in incomplete_connections if not conn.road]
        if untouched_connections:
            target_connection = random.choice(untouched_connections)
        else:
            target_connection = random.choice(incomplete_connections)

        # --- ACUMULACIÓN DE MÉTRICAS ---
        path, nodes_expanded, max_depth = self._dfs_for_one_color(board, target_connection)
        self.total_nodes_expanded += nodes_expanded
        self.max_search_depth_overall = max(self.max_search_depth_overall, max_depth)

        if path:
            target_connection.clean_road()
            for point in path:
                target_connection.add_to_road(point)
            return path[-1]
        else:
            board_state = self._get_hashable_state(board)
            self.failed_states.add(board_state)
            print(f"DFS Player: Atascado en '{target_connection.name}'. Reiniciando. Memoria: {len(self.failed_states)}")
            for conn in board.connections:
                conn.clean_road()
            return board.connections[0].points[0]

    # --- NUEVO MÉTODO PARA GENERAR REPORTES ---
    def _generate_reports(self, final_board: FlowFreeBoard, level_name: str):
        """Crea los archivos de salida .txt y .csv con las métricas de rendimiento."""
        
        running_time = time.monotonic() - self.start_time
        _, max_ram_usage = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        max_ram_usage /= 1024**2  # Convertir a MB

        cost_of_path = sum(len(conn.road) - 1 for conn in final_board.connections)
        search_depth = cost_of_path # La profundidad de la solución es el total de celdas del camino

        path_to_goal_matrix = [['' for _ in range(final_board.columns)] for _ in range(final_board.rows)]
        for conn in final_board.connections:
            char = next(key for key, value in Connection.NAMES.items() if value == conn.name)
            for (px, py) in conn.road:
                path_to_goal_matrix[py][px] = char

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # --- Escribir archivo .txt ---
        txt_filename = os.path.join(output_dir, f"{level_name.replace('.txt', '')}.txt")
        with open(txt_filename, 'w') as f:
            f.write(f"path_to_goal: {path_to_goal_matrix}\n")
            f.write(f"cost_of_path: {cost_of_path}\n")
            f.write(f"nodes_expanded: {self.total_nodes_expanded}\n")
            f.write(f"search_depth: {search_depth}\n")
            f.write(f"max_search_depth: {self.max_search_depth_overall}\n")
            f.write(f"running_time: {running_time:.8f}\n")
            f.write(f"max_ram_usage: {max_ram_usage:.8f}\n")
        print(f"Reporte .txt guardado en: {txt_filename}")

        # --- Escribir archivo .csv ---
        csv_filename = os.path.join(output_dir, "benchmark.csv")
        file_exists = os.path.isfile(csv_filename)
        
        with open(csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            headers = ["Algorithm-Level", "cost_of_path", "nodes_expanded", "search_depth", "max_search_depth", "running_time", "max_ram_usage"]
            if not file_exists:
                writer.writerow(headers)
            
            row_data = [
                f"DFS-{level_name.replace('.txt', '')}",
                cost_of_path,
                self.total_nodes_expanded,
                search_depth,
                self.max_search_depth_overall,
                f"{running_time:.8f}",
                f"{max_ram_usage:.8f}"
            ]
            writer.writerow(row_data)
        print(f"Resultados añadidos a: {csv_filename}")