from menu import Menu
from color import Color
from board import Board
from cargar_txt import load
from control import Control
import os
# from player import Player
    
class Connection:
    """
    Representa una conexión entre dos puntos en el tablero de Flow Free.
    Cada conexión tiene un color y dos puntos (inicio y fin).
    La conexion se completa cuando se traza un camino entre los dos puntos.
    Colores disponibles: Azul, Rojo, Verde, Amarillo, Magenta, Cyan, Naranja.
    
    Parámetros:
    color: str -> 'A', 'R', 'V', 'Y', 'M', 'C', 'N'
    point_1: tuple -> (column, row)
    point_2: tuple -> (column, row)
    """
    # A: Azul, R: Rojo, V: Verde, Y: Amarillo, M: Magenta, C: Cyan, N: Naranja
    NAMES = {"A":"blue", "R":"red", "V":"green", "Y":"yellow",  "M":"magenta", "C":"cyan", "N":"orange"}
    COLORS = {"A":Color.BLUE, "R":Color.RED, "V":Color.GREEN, "Y":Color.YELLOW, "M":Color.MAGENTA, "C":Color.CYAN, "N":Color.ORANGE}
    
    def __init__(self, color:str, point_1:tuple, point_2:tuple) -> None:
        self.name = self.NAMES.get(color, None)
        if not self.name:
            raise ValueError(f"Color '{color}' no es válido. Colores válidos: {list(self.NAMES.keys())}")
        self.color = self.COLORS.get(color)
        self.points = (point_1, point_2) # Tuplas (column, row)
        self.road = [] # Lista de tuplas (column, row) que representan el camino de la conexión
        self.is_completed = False
        
    def add_to_road(self, point:tuple) -> None:
        """
        Agrega un punto al camino de la conexión.
        
        Parámetros:
        point: tuple -> (column, row)
        """
        if point not in self.road:
            self.road.append(point)
            self.check_completion()
            
    def check_completion(self) -> None:
        """
        Verifica si la conexión está completa (si el camino conecta ambos puntos).
        """
        if self.points[0] in self.road and self.points[1] in self.road:
            self.is_completed = True
        else:
            self.is_completed = False
    
    def pop_road(self) -> None:
        """
        Elimina el último punto del camino de la conexión.
        """
        if self.road:
            self.road.pop()
        self.is_completed = False
            
    def break_road(self, point:tuple) -> None:
        """
        Rompe el camino de la conexión, eliminando todos los puntos del camino despues de ese punto.
        """
        if point in self.road:
            index = self.road.index(point)
            self.road = self.road[:index]
        self.is_completed = False
        
    def clean_road(self) -> None:
        """
        Limpia todo el camino de la conexión.
        """
        self.road = []
        self.is_completed = False
        
class FlowFreeBoard(Board):
    
    def __init__(self, path:str) -> None:
        self.connections = []
        self.board = load(path, as_list=True)
        rows = len(self.board)
        columns = len(self.board[0]) if rows > 0 else 0
        super().__init__(rows, columns)
        self._complete_board()         
        self.length = sum(1 for r in range(rows) for c in range(columns) if self.grid[r][c] is not None) - len(self.connections)
        self.flow_free_moves = 0

                    
    def _complete_board(self) -> None:
        """
        Marca una conexión como completa y actualiza el tablero.
        """
        for r in range(self.rows):
            for c in range(self.columns):
                cell = self.board[r][c]
                if cell == '.':
                    cell = '.' # Celda vacía
                elif cell == '#':
                    cell = None # Pared
                else:
                    if cell not in Connection.NAMES.keys():
                        raise ValueError(f"Carácter '{cell}' en la posición ({c},{r}) no es válido. Carácteres válidos: {list(Connection.NAMES.keys())} + '.' + '#'")
                    
                    if Connection.NAMES[cell] in [conn.name for conn in self.connections]:
                        # Si ya existe una conexión con ese color, asignar el segundo punto
                        for conn in self.connections:
                            if conn.name == Connection.NAMES[cell] and conn.points[1] is None:
                                conn.points = (conn.points[0], (c,r))
                                cell = conn
                                break
                    else:
                        # Crear una nueva conexión con el primer punto
                        cell = Connection(cell, (c,r), None) # El segundo punto se asignará al encontrar el otro punto en el archivo
                        self.connections.append(cell)
                self.grid[r][c] = cell
    
    def _validate_cell(self, x, y) -> bool:
        if not super()._validate_cell(x, y):
            return False
        if self.grid[y][x] is None:
            return False # Pared
        return True
    
    def _get_selectable_cells(self) -> list[tuple[int, int]]:
        points_cell = [point for conn in self.connections for point in conn.points]
        x_cells = [conn.road[-1] for conn in self.connections if conn.road]
        cells = points_cell + x_cells
        cells = list(set(cells)) # Eliminar duplicados
        cells.sort(key=lambda t: (t[1], t[0]), reverse=False)
        return cells 
    
    def percentage_filled(self) -> float:
        """
        Devuelve el porcentaje del tablero que ha sido llenado.
        """
        cells_filled = sum(len(conn.road)-1 for conn in self.connections if conn.road)
        return (cells_filled * 100 // self.length)
    
    def show(self, highlight_cell = tuple[int, int]) -> None:
        """
        Muestra el tablero en la consola.
        """
        os.system('cls')
        percentage = self.percentage_filled()
        
        print(f" Moves: {self.flow_free_moves}", end=' | ')
        print(f"Pipe: {percentage}%")
        print(f"{'-'* (self.columns* 4)}-")
        for y in range(self.rows):
            for x in range(self.columns):
                
                # Highlight current cell
                if (x, y) == highlight_cell and isinstance(self.grid[y][x], Connection):
                    print(f"| {Color.BOLD}{self.grid[y][x].color}0{Color.RESET} ", end='')
                
                elif isinstance(self.grid[y][x], Connection):
                    if self.grid[y][x].is_completed:
                            print(f"| {Color.BOLD}{self.grid[y][x].color}O{Color.RESET} ", end='')
                    else:
                        print(f"| {self.grid[y][x].color}O{Color.RESET} ", end='')
                    
                elif (x, y) in [point for conn in self.connections for point in conn.road]:
                    for conn in self.connections:
                        if (x, y) in conn.road:
                            # Celda llena que es parte de una conexión
                            if (x, y) == highlight_cell:
                                print(f"| {Color.BOLD}{conn.color}X{Color.RESET} ", end='')
                            elif conn.is_completed:
                                print(f"| {Color.BOLD}{conn.color}x{Color.RESET} ", end='')    
                            else:
                                print(f"| {conn.color}x{Color.RESET} ", end='')
                            break
                
                elif self.grid[y][x] is None:
                    print("| # ", end='')
                
                else:
                    print("|   ", end='')
            
            print("|")
            print(f"{'-'* (self.columns* 4)}-")        

        if percentage == 100: print(f"{Color.GREEN}¡Felicidades! Has completado el nivel.{Color.RESET}") 
        
class FlowFree:
       
    def __init__(self, board:Board) -> None:
        self.board = board
        self.last_color_position = None
        self.last_move = None
        
    
    def play(self, player) -> None:
        
        while True:
            
            percentage = self.board.percentage_filled()
            
            if percentage == 100:
                self.board.show()
                break
            
            
            move = player.play(self.board)
            
            if not move:
                print("Juego terminado.")
                break
            
            x, y = move    
            if not self.board._validate_cell(x, y):
                continue
            
            elif move == self.last_move:
                if move == self.last_color_position:
                    self.board.grid[y_color][x_color].pop_road()
                self.last_move = None
                self.last_color_position = None
                player.position = None
                continue
            
            elif self.last_color_position and move == self.last_color_position:
                x_color, y_color = self.last_color_position
                self.board.grid[y_color][x_color].pop_road()
                # self.last_color_position = None
                self.last_move = move
                player.position = move
                continue
            
            elif not self.last_color_position:
                if isinstance(self.board.grid[y][x], Connection):
                    self.last_color_position = (x, y)
                    self.board.grid[y][x].clean_road()
                    self.board.grid[y][x].add_to_road(move)
                else:
                    for conn in self.board.connections:
                        if (x, y) in conn.road:
                            # Romper la conexión en ese punto
                            self.last_color_position = conn.points[0]
                            break
                player.position = move
                continue
            
            elif isinstance(self.board.grid[y][x], Connection):
                x_color, y_color = self.last_color_position
                if self.board.grid[y][x].name != self.board.grid[y_color][x_color].name:
                    continue # Not same color
                
                self.board.grid[y][x].add_to_road(move)
                self.board.grid[y][x].check_completion()
                self.last_color_position = None
                player.position = None
                self.board.flow_free_moves += 1
                continue

            
            elif (x, y) in [point for conn in self.board.connections for point in conn.road]:
                for conn in self.board.connections:
                    if (x, y) in conn.road:
                        # Romper la conexión en ese punto
                        conn.break_road((x, y))
                        break
                
            player.position = move
            x_color, y_color = self.last_color_position
            self.last_move = move
            self.board.grid[y_color][x_color].add_to_road(move)
    
    def get_state(self, format: str = "raw") -> any:
        """
        Devuelve el estado del tablero en el formato solicitado.
        - 'raw': lista de listas con valores simples (para algoritmos)
        - 'visual': representación para humanos (colores, símbolos)
        """
        if format == "raw":
            return [[self._cell_value(cell) for cell in row] for row in self.grid]
        elif format == "visual":
            # Podrías devolver una cadena con el tablero renderizado
            return self._render_board()
        else:
            raise ValueError(f"Formato desconocido: {format}")
    
    
    
# --- IGNORE ---
if __name__ == '__main__':
    board = FlowFreeBoard("levels/5x5_4C_1.txt")
    board.show()