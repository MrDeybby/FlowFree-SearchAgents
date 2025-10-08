# algorithms/bfs.py

from collections import deque
import time
import tracemalloc

from game.flow_free import FlowFreeBoard, Connection
from algorithms.metrics import Metrics


class BFSPlayer(Metrics):
    """
    BFS multinivel y round-robin por conexión (sin heurísticas).
    - Inicializa una cola FIFO por cada conexión incompleta.
    - Expande por turnos (round-robin) una capa por conexión, respetando UDLR.
    - Cuando la primera conexión encuentra ruta, aplica ese camino y termina el ciclo.
    - Si todas acaban sin ruta útil en este estado, se reinicia (limpia trazos).
    """

    def __init__(self):
        super().__init__(name="BFS")
        self.failed_states = set()

    # ---------------- Utilidades ----------------
    def _get_hashable_state(self, board: FlowFreeBoard):
        return tuple(map(tuple, board.get_state()))

    @staticmethod
    def _udlr_neighbors(x: int, y: int):
        # Up, Down, Left, Right
        return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

    # ---------------- Núcleo BFS round-robin ----------------
    def _build_occupancy_for(self, board: FlowFreeBoard, target: Connection):
        """
        Retorna las celdas ocupadas por otras conexiones distintas de 'target'.
        """
        occupied = set()
        for conn in board.connections:
            if conn is not target:
                occupied.update(conn.road)
                occupied.update(conn.points)
        return occupied

    def _bfs_round_robin(self, board: FlowFreeBoard):
        """
        Crea una cola por cada conexión incompleta y expande por turnos.
        Devuelve (target_connection, path, nodes_expanded, max_depth)
        o (None, None, nodes_expanded, max_depth) si nadie encontró ruta.
        """
        # Preparar frentes por conexión
        targets = [c for c in board.connections if not c.is_completed]
        if not targets:
            return None, None, 0, 0

        frontiers = {}
        visited = {}
        parents = {}  # opcional, acá guardamos el path inline
        end_points = {}
        nodes_expanded = 0
        max_depth = 0

        for conn in targets:
            start, goal = conn.points[0], conn.points[1]
            end_points[conn] = goal
            frontiers[conn] = deque([(start, [start])])
            visited[conn] = {start}
            parents[conn] = {}  # no imprescindible; usamos camino en la tupla

        # Round-robin: en cada “vuelta” se expande una capa de cada conexión
        while True:
            progressed = False

            for conn in targets:
                if not frontiers[conn]:
                    continue

                progressed = True  # al menos una cola pudo intentar expandir

                # Expandimos toda la “capa actual” de esta conexión
                layer_size = len(frontiers[conn])
                goal = end_points[conn]
                occupied_others = self._build_occupancy_for(board, conn)

                for _ in range(layer_size):
                    current, path = frontiers[conn].popleft()
                    nodes_expanded += 1
                    if len(path) > max_depth:
                        max_depth = len(path)

                    if current == goal:
                        # Encontramos ruta para esta conexión
                        return conn, path, nodes_expanded, max_depth

                    cx, cy = current
                    for nx, ny in self._udlr_neighbors(cx, cy):
                        # Dentro del tablero
                        if not board._validate_cell(nx, ny):
                            continue
                        nxt = (nx, ny)

                        # No revisitar y no pisar otros caminos/endpoints
                        if nxt in visited[conn] or nxt in occupied_others:
                            continue

                        # Evitar lazos con el propio camino parcial
                        if nxt in path:
                            continue

                        visited[conn].add(nxt)
                        frontiers[conn].append((nxt, path + [nxt]))

            # Si en una vuelta completa nadie avanzó (todas colas vacías), no hay ruta
            if not progressed:
                return None, None, nodes_expanded, max_depth

    # ---------------- Bucle principal ----------------
    def play(self, board: FlowFreeBoard, level_name: str = "unknown_level"):
        """
        Orquesta BFS multinivel:
        - Si el tablero está completo pero no 100% lleno, registra estado fallido y reinicia.
        - Si está 100% lleno, genera reporte y finaliza.
        - Ejecuta BFS round-robin entre TODAS las conexiones incompletas hasta que una encuentre ruta.
        - Aplica el primer camino encontrado y retorna la última celda de ese camino.
        """
        # Iniciar métricas globales si es la primera llamada
        if self.start_time is None:
            self.start_time = time.monotonic()
            tracemalloc.start()

        all_completed = all(c.is_completed for c in board.connections)
        filled = board.percentage_filled()

        # Caso callejón: todo “completado” pero no 100% lleno
        if all_completed and filled < 100:
            st = self._get_hashable_state(board)
            self.failed_states.add(st)
            for c in board.connections:
                c.clean_road()
            # Convención: devolver una celda válida para que el motor continúe
            return board.connections[0].points[0]

        # Caso solución: 100% lleno
        if all_completed and filled == 100:
            self._generate_reports(board, level_name)
            return None

        # Ejecutar BFS round-robin entre todas las conexiones incompletas
        target_conn, path, nodes_expanded, max_depth = self._bfs_round_robin(board)

        # Actualizar métricas globales
        self.total_nodes_expanded += nodes_expanded
        if max_depth > self.max_search_depth_overall:
            self.max_search_depth_overall = max_depth

        if path:
            # Aplicar el primer camino válido encontrado
            target_conn.clean_road()
            for p in path:
                target_conn.add_to_road(p)
            target_conn.check_completion()
            return path[-1]

        # Ninguna conexión encontró ruta en este estado -> memoriza y reinicia
        st = self._get_hashable_state(board)
        self.failed_states.add(st)
        for c in board.connections:
            c.clean_road()
        return board.connections[0].points[0]
