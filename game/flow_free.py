from menu import Menu
from color import Color
from board import Board
from cargar_txt import load
from control import Control
# from player import Player
    
class Connection:
    """
    Representa una conexión entre dos puntos en el tablero de Flow Free.
    Cada conexión tiene un color y dos puntos (inicio y fin).
    La conexion se completa cuando se traza un camino entre los dos puntos.
    Colores disponibles: Azul, Rojo, Verde, Amarillo, Magenta, Cyan, Naranja.
    
    Parámetros:
    color: str -> 'A', 'R', 'V', 'Y', 'M', 'C', 'N'
    point_1: tuple -> (row, col)
    point_2: tuple -> (row, col)
    """
    # A: Azul, R: Rojo, V: Verde, Y: Amarillo, M: Magenta, C: Cyan, N: Naranja
    NAMES = {"A":"blue", "R":"red", "V":"green", "Y":"yellow",  "M":"magenta", "C":"cyan", "N":"orange"}
    COLORS = {"A":Color.BLUE, "R":Color.RED, "V":Color.GREEN, "Y":Color.YELLOW, "M":Color.MAGENTA, "C":Color.CYAN, "N":Color.ORANGE}
    
    def __init__(self, color:str, point_1:tuple, point_2:tuple) -> None:
        self.name = self.NAMES.get(color, None)
        if not self.name:
            raise ValueError(f"Color '{color}' no es válido. Colores válidos: {list(self.NAMES.values())}")
        self.color = self.COLORS.get(color)
        self.points = (point_1, point_2) # Tuplas (row, col)
        self.road = [] # Lista de tuplas (row, col) que representan el camino de la conexión
        self.completed = False
        
    def add_to_road(self, point:tuple) -> None:
        """
        Agrega un punto al camino de la conexión.
        
        Parámetros:
        point: tuple -> (row, col)
        """
        if point not in self.road:
            self.road.append(point)
            self.check_completion()
            
    def check_completion(self) -> None:
        """
        Verifica si la conexión está completa (si el camino conecta ambos puntos).
        """
        if self.points[0] in self.road and self.points[1] in self.road:
            self.completed = True
        else:
            self.completed = False
            
    def break_road(self, point:tuple) -> None:
        """
        Rompe el camino de la conexión, eliminando todos los puntos del camino despues de ese punto.
        """
        if point in self.road:
            index = self.road.index(point)
            self.road = self.road[:index]
        self.completed = False
        
        
class FlowFreeBoard(Board):
    
    def __init__(self, path:str) -> None:
        self.connections = []
        self.filled_cells = 0
        self.board = load(path, as_list=True)
        rows = len(self.board)
        columns = len(self.board[0]) if rows > 0 else 0
        super().__init__(rows, columns)
        self._complete_board()         
        self.length = sum(1 for r in range(rows) for c in range(columns) if self.grid[r][c] is not None)
        self.boolean_grid = [[False if self.grid != None else None for c in range(columns)] for r in range(rows)]
        
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
                        raise ValueError(f"Carácter '{cell}' en la posición ({r},{c}) no es válido. Carácteres válidos: {list(Connection.NAMES.keys())} + '.' + '#'")
                    
                    if Connection.NAMES[cell] in [conn.name for conn in self.connections]:
                        # Si ya existe una conexión con ese color, asignar el segundo punto
                        for conn in self.connections:
                            if conn.name == Connection.NAMES[cell] and conn.points[1] is None:
                                conn.points = (conn.points[0], (r,c))
                                cell = conn
                                break
                    else:
                        # Crear una nueva conexión con el primer punto
                        cell = Connection(cell, (r,c), None) # El segundo punto se asignará al encontrar el otro punto en el archivo
                        self.connections.append(cell)
                self.grid[r][c] = cell
    
    def _validate_cell(self, x, y) -> bool:
        if not super()._validate_cell(x, y):
            return False
        if self.grid[y][x] is None:
            return False # Pared
        # if isinstance(self.grid[y][x], Connection):
        #     return False # Punto de conexión
        return True
    
    def _get_selectable_cells(self) -> list[tuple[int, int]]:
        cells = []
        for r in range(self.rows):
            for c in range(self.columns):
                if isinstance(self.grid[r][c], Connection):
                    cells.append((c, r))
        return cells  
    
    def show(self, highlight_cell = tuple[int, int]) -> None:
        """
        Muestra el tablero en la consola.
        """
        print([conn.road for conn in self.connections])
        print(f"{'-'* (self.columns* 4)}-")
        for y in range(self.rows):
                for x in range(self.columns):
                    
                    # Highlight current cell
                    if (x, y) == highlight_cell and isinstance(self.grid[y][x], Connection):
                        print(f"| {Color.BOLD}{self.grid[y][x].color}0{Color.RESET} ", end='')
                    
                    elif isinstance(self.grid[y][x], Connection):
                        print(f"| {self.grid[y][x].color}O{Color.RESET} ", end='')
                        
                    elif (x, y) in [point for conn in self.connections for point in conn.road]:
                        for conn in self.connections:
                            if (x, y) in conn.road:
                                
                                if (x, y) == highlight_cell:
                                    print(f"| {Color.BOLD}{conn.color}X{Color.RESET} ", end='')
                                    
                                else:
                                    print(f"| {Color.BOLD}{conn.color}x{Color.RESET} ", end='')
                                break
                    
                         
                    elif (x, y) == highlight_cell:
                        print(f"| {Color.BOLD}X{Color.RESET} ", end='') 
                        
                    # elif (x, y) == highlight_cell:
                    #     print(f"| {Color.BOLD}{self.grid[y][x].color}X{Color.RESET} ", end='') 
                            
                    
                        
                    elif self.grid[y][x] is None:
                        print("| X ", end='')
                    elif self.grid[y][x] == '.':
                        print("|   ", end='')
                        
                    # elif (x, y) in [point for conn in self.connections for point in conn.road]:
                    #     # Celda llena que es parte de una conexión
                    #     for conn in self.connections:
                    #         if (x, y) in conn.road:
                    #             print(f"| {conn.color}*{Color.RESET} ", end='')
                    #             break
                    
                    elif self.grid[y][x] == 'X':
                        print("| x ", end='')
                print("|")
                print(f"{'-'* (self.columns* 4)}-")        

class FlowFree:
    
    board = FlowFreeBoard("levels/5_x_5_4C_1.txt")
    
    def __init__(self, board:Board) -> None:
        self.board = board
        self.last_color_position = None
        self.last_move = None
    
    def play(self, player) -> None:
        
        while True:
            move = player.play(self.board)
            
            if not move:
                print("Juego terminado.")
                break
            
            x, y = move
            
            if not self.board._validate_cell(x, y):
                continue
            
            if not self.last_color_position:
                self.last_color_position = (x, y)
                self.board.grid[y][x].add_to_road(move)
                player.position = move
                continue
            
            if isinstance(self.board.grid[y][x], Connection) and self.board.grid[y][x].name == self.last_color_position:
                self.board.grid[y][x].add_to_road(move)
                self.last_color_position = None
                player.position = None
                continue
                    
            player.position = move
            x_color, y_color = self.last_color_position
            self.board.grid[y_color][x_color].add_to_road(move)
            self.board.grid[y][x] = 'X' # Marcar la celda como llena
            self.board.filled_cells += 1
    
    # def get_state(self, format: str = "raw") -> any:
    #     """
    #     Devuelve el estado del tablero en el formato solicitado.
    #     - 'raw': lista de listas con valores simples (para algoritmos)
    #     - 'visual': representación para humanos (colores, símbolos)
    #     """
    #     if format == "raw":
    #         return [[self._cell_value(cell) for cell in row] for row in self.grid]
    #     elif format == "visual":
    #         # Podrías devolver una cadena con el tablero renderizado
    #         return self._render_board()
    #     else:
    #         raise ValueError(f"Formato desconocido: {format}")
        
# --- IGNORE ---
if __name__ == '__main__':
    board = FlowFreeBoard("levels/5_x_5_4C_1.txt")
    board.show()