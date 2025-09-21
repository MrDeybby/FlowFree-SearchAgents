from menu import Menu
from color import Color
from board import Board
from cargar_txt import load

class FlowFree:
    
    @staticmethod
    
    def play():
        pass
    

class Connection:
    """
    Representa una conexión entre dos puntos en el tablero de Flow Free.
    Cada conexión tiene un color y dos puntos (inicio y fin).
    La conexion se completa cuando se traza un camino entre los dos puntos.
    Colores disponibles: Azul, Rojo, Verde, Amarillo, Magenta, Cyan, Naranja.
    """
    # A: Azul, R: Rojo, V: Verde, Y: Amarillo, M: Magenta, C: Cyan, N: Naranja
    NAMES = {"A":"blue", "R":"red", "V":"green", "Y":"yellow",  "M":"magenta", "C":"cyan", "N":"orange"}
    COLORS = {"A":Color.BLUE, "R":Color.RED, "V":Color.GREEN, "Y":Color.YELLOW, "M":Color.MAGENTA, "C":Color.CYAN, "N":Color.ORANGE}
    
    def __init__(self, color:str, point_1:tuple, point_2:tuple) -> None:
        """
        Representa una conexión entre dos puntos en el tablero de Flow Free.
        
        Parámetros:
        color: str -> 'A', 'R', 'V', 'Y', 'M', 'C', 'N'
        point_1: tuple -> (row, col)
        point_2: tuple -> (row, col)
        """
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
        cols = len(self.board[0]) if rows > 0 else 0
        super().__init__(rows, cols)
        self._complete_board()         
        self.length = sum(1 for r in range(rows) for c in range(cols) if self.grid[r][c] is not None)
        self.boolean_grid = [[False if self.grid != None else None for c in range(cols)] for r in range(rows)]
        
    def _complete_board(self) -> None:
        """
        Marca una conexión como completa y actualiza el tablero.
        """
        for r in range(self.rows):
            for c in range(self.cols):
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
              
# --- IGNORE ---
if __name__ == '__main__':
    board = FlowFreeBoard("levels/5_x_5_4C_1.txt")
    # print([[cell.color if isinstance(cell, Connection) else cell for cell in row] for row in board.grid])
    
    for row in board.grid:
        for cell in row:
            if isinstance(cell, Connection):
                print(f"{cell.color}o{Color.RESET}", end='')
            else:
                if cell is None:
                    print(Color.FILLED_SYMBOL, end='')
                else:
                    print(Color.EMPTY_SYMBOL, end='')
        print()