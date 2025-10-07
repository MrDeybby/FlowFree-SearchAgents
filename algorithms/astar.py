import heapq
import time
from collections import deque
import random
import math
import tracemalloc


from game.flow_free import FlowFreeBoard, Connection
from algorithms.metrics import Metrics

class AStarPlayer(Metrics):
    def __init__(self):
        super().__init__(name="AStar")
        self.current_path_connections = {}
        # Para aprender de los estados que no llevan a una solución del 100%
        self.failed_states = set()

    # ESTRATEGIA PRINCIPAL: REINICIO ALEATORIO CON MEMORIA
    def play(self, board: FlowFreeBoard, level_name: str = "unknown_level") -> tuple | None:
        if self.start_time is None:
            self.start_time = time.monotonic()
            tracemalloc.start()

        all_completed = all(conn.is_completed for conn in board.connections)

        # CASO 1: CALLEJÓN SIN SALIDA (COMPLETO PERO NO LLENO)
        if all_completed and board.percentage_filled() < 100:
            board_state_tuple = tuple("".join(map(str, row)) for row in board.get_state())
            if board_state_tuple not in self.failed_states:
                print(f"AI Player: Nuevo callejón sin salida detectado. Memorizando...")
                self.failed_states.add(board_state_tuple)
            
            print(f"Tamaño de la memoria de fallos: {len(self.failed_states)}")
            for conn in board.connections:
                conn.clean_road()
            all_completed = False

        # CASO 2: SOLUCIÓN ENCONTRADA
        if all_completed and board.percentage_filled() == 100:
            print("A* Player: ¡Solución encontrada!")
            self._generate_reports(board, level_name)
            return None

        # Lógica para elegir el siguiente movimiento
        incomplete_connections = [conn for conn in board.connections if not conn.is_completed]
        if not incomplete_connections:
            return None

        target_connection = random.choice(incomplete_connections)
        
        # Llama a la herramienta A* para encontrar un camino
        path, nodes_expanded, max_depth = self._astar_search(board, target_connection)
        
        self.total_nodes_expanded += nodes_expanded
        self.max_search_depth_overall = max(self.max_search_depth_overall, max_depth)

        if path:
            # Si se encuentra un camino, se aplica
            target_connection.clean_road()
            for p in path:
                target_connection.add_to_road(p)
            target_connection.check_completion()
            return path[-1]
        else:
            # CASO 3: ATASCO (A* NO ENCUENTRA CAMINO)
            print(f"AI atascado en '{target_connection.name}'.")
            board_state_tuple = tuple("".join(map(str, row)) for row in board.get_state())
            if board_state_tuple not in self.failed_states:
                 self.failed_states.add(board_state_tuple)
            
            print(f"Tamaño de la memoria de fallos: {len(self.failed_states)}")
            for conn in board.connections:
                conn.clean_road()
            return board.connections[0].points[0]

    # HEURÍSTICA COMBINADA
    def _calculate_combined_heuristic(self, p1: tuple[int, int], p2: tuple[int, int], board: 'FlowFreeBoard') -> float:
        """
        Calcula una heurística combinada que ahora incluye una "Bonificación por Exploración".
        """
        w1 = 0.2# Peso para Manhattan
        w2 = 0.2  # Peso para Penalización por Encierro
        w3 = 0.1  # Peso para Euclidiana
        w4 = 0.5# Peso para Bonificación por Exploración

        # 1. Heurística de Manhattan (h1)
        h1 = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        max_h1 = board.rows + board.columns
        h1_norm = h1 / max_h1 if max_h1 > 0 else 0
        
        # 2. Heurística de Penalización por Encierro (h2)
        x, y = p1
        occupied_neighbors = 0
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if not board._validate_cell(nx, ny):
                occupied_neighbors += 1
            else:
                is_other_path = False
                for conn in board.connections:
                    is_endpoint = isinstance(board.grid[p2[1]][p2[0]], Connection)
                    if (nx, ny) in conn.road and (not is_endpoint or conn is not board.grid[p2[1]][p2[0]]):
                        is_other_path = True
                        break
                if is_other_path:
                    occupied_neighbors += 1
        h2 = occupied_neighbors
        h2_norm = h2 / 4.0

        # 3. Heurística Euclidiana (h3)
        h3 = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        max_h3 = math.sqrt(board.rows**2 + board.columns**2)
        h3_norm = h3 / max_h3 if max_h3 > 0 else 0

        # 4. Bonificación por Exploración (h4)
        center_x, center_y = (board.columns - 1) / 2.0, (board.rows - 1) / 2.0
        h4 = math.sqrt((p1[0] - center_x)**2 + (p1[1] - center_y)**2)
        max_h4 = math.sqrt(center_x**2 + center_y**2)
        h4_norm = h4 / max_h4 if max_h4 > 0 else 0
        
        # Combinación Final (se resta h4 para que sea una recompensa)
        final_heuristic = (w1 * h1_norm) + (w2 * h2_norm) + (w3 * h3_norm) - (w4 * h4_norm)
        return final_heuristic

    # ALGORITMO DE BÚSQUEDA A*
    def _astar_search(self, initial_board: FlowFreeBoard, target_connection: Connection):
        nodes_expanded = 0
        max_depth = 0
        start_point, end_point = target_connection.points

        open_set = []
        heuristic_cost = self._calculate_combined_heuristic(start_point, end_point, initial_board)
        heapq.heappush(open_set, (heuristic_cost, start_point, [start_point]))

        g_score = {start_point: 0}
        visited_states = set()

        while open_set:
            _, current_point, path = heapq.heappop(open_set)
            nodes_expanded += 1
            max_depth = max(max_depth, len(path))

            if current_point == end_point:
                return path, nodes_expanded, max_depth

            state_tuple = (current_point, tuple(path))
            if state_tuple in visited_states:
                continue
            visited_states.add(state_tuple)

            x, y = current_point
            for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if not initial_board._validate_cell(nx, ny):
                    continue
                
                neighbor_point = (nx, ny)
                if neighbor_point in path:
                    continue

                is_blocked = any(
                    conn != target_connection and (neighbor_point in conn.road or neighbor_point in conn.points)
                    for conn in initial_board.connections
                )
                if is_blocked:
                    continue
                
                tentative_g_score = g_score.get(current_point, float('inf')) + 1
                if tentative_g_score < g_score.get(neighbor_point, float('inf')):
                    g_score[neighbor_point] = tentative_g_score
                    f_score = tentative_g_score + self._calculate_combined_heuristic(neighbor_point, end_point, initial_board)
                    new_path = path + [neighbor_point]
                    heapq.heappush(open_set, (f_score, neighbor_point, new_path))

        return None, nodes_expanded, max_depth