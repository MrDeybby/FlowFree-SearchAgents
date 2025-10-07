from game.menu import Menu
from game.color import Color
from game.board import Board
from game.cargar_txt import load
from game.control import Control
import os, time
from game.player import HumanPlayer


# The `Connection` class represents a connection between two points on a Flow Free board with methods
# to manage the path and check completion status.
class Connection:
    # A: Azul, R: Rojo, V: Verde, Y: Amarillo, M: Magenta, C: Cyan, N: Naranja
    NAMES = {"A":"blue", "R":"red", "V":"green", "Y":"yellow",  "M":"magenta", 
             "C":"cyan", "N":"orange", "G":"gray", "L":"lime", "P":"purple",
             "D":"dark blue", "O":"ocre", "B":"light blue",
             "F":"fucsia"}
    COLORS = {"A":Color.BLUE, "R":Color.RED, "V":Color.GREEN,
              "Y":Color.YELLOW, "M":Color.MAGENTA, "C":Color.CYAN,
              "N":Color.ORANGE, "G":Color.GRAY, "L":Color.LIME,
              "P":Color.PURPLE, "D":Color.DARK_BLUE, "O":Color.OCRE,
              "B":Color.LIGHT_BLUE, "F":Color.FUCSIA}
    
    def __init__(self, color:str, point_1:tuple, point_2:tuple) -> None:
        """
        Initializes an object with a specified color, two points, a road list, and a
        completion status flag.
        
        :param color: The `color` parameter in the `__init__` method is a string that represents the color
        of an object. It is used to initialize the object with a specific color
        :type color: str
        :param point_1: The `point_1` parameter in the `__init__` method is a tuple that represents a point
        on a grid. The tuple should contain two values: the column and row of the point. For example, `(2,
        3)` could represent a point at column 2 and row 3
        :type point_1: tuple
        :param point_2: The `point_2` parameter in the `__init__` method is a tuple that represents a point
        in a coordinate system. It is used to define the second point of a line segment or connection in the
        context of the code snippet you provided. The tuple likely contains two values, such as
        :type point_2: tuple
        """
        self.name = self.NAMES.get(color, None)
        if not self.name:
            raise ValueError(f"Color '{color}' no es válido. Colores válidos: {list(self.NAMES.keys())}")
        self.color = self.COLORS.get(color)
        self.points = (point_1, point_2) # Tuplas (column, row)
        self.road = [] # Lista de tuplas (column, row) que representan el camino de la conexión
        self.is_completed = False
        
    def add_to_road(self, point:tuple) -> None:
        """
        Adds a point to a road list and checks for completion.
        
        :param point: The `add_to_road` method takes a tuple `point` as a parameter. This method adds the
        `point` to the `road` list if it is not already present in the list. After adding the `point`, it
        calls the `check_completion` method
        :type point: tuple
        """

        if point not in self.road:
            self.road.append(point)
            self.check_completion()
            
    def check_completion(self) -> None:
        """
        Check if the connection is complete (if the path connects both colors points).
        """
        if self.points[0] in self.road and self.points[1] in self.road:
            self.is_completed = True
        else:
            self.is_completed = False
    
    def pop_road(self) -> None:
        """
        Delete the last point of the path
        """
        if self.road:
            self.road.pop()
        self.is_completed = False
            
    def break_road(self, point:tuple) -> None:
        """
        Breaks the path of the connection, removing all points from the path after that point.
        """
        if point in self.road:
            index = self.road.index(point)
            self.road = self.road[:index]
        self.is_completed = False
        
    def clean_road(self) -> None:
        """
        Cleans the entire connection path.
        """
        self.road = []
        self.is_completed = False

# The `FlowFreeBoard` class represents a board for the Flow Free game, allowing players to make
# connections between points of the same color.
class FlowFreeBoard(Board):
    
    def __init__(self, path:str) -> None:
        """
        Initializes an object with attributes related to a game board and
        connections.
        
        :param path: The `path` parameter is expected to be a string that represents the path
        to a file. This file is then loaded using the `load` function with the
        `as_list` parameter set to `True`.
        :type path: str
        """
        self.connections = []
        self.board = load(path, as_list=True)
        rows = len(self.board)
        columns = len(self.board[0]) if rows > 0 else 0
        super().__init__(rows, columns)
        self._complete_board()         
        # The code calculates the grid length by counting the number of elements that are not equal to "#"
        # and subtracting the length of the netlist. This is used to calculate the missing percentage.
        self.length = sum(1 for r in range(rows) for c in range(columns) if self.grid[r][c] is not "#") - len(self.connections)
        self.flow_free_moves = 0        
              
    def _complete_board(self) -> None:
        """
        Marca una conexión como completa y actualiza el tablero.
        """
        for r in range(self.rows):
            for c in range(self.columns):
                cell = self.board[r][c]
                if cell != '.' and cell != '#':
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
        if self.grid[y][x] == "#":
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
    
    def show(self, highlight_cell:tuple[int, int] = None) -> None:
        """
        Displays a game board in the console with the ability to highlight a
        specific cell.
        
        :param highlight_cell: Specify the cell that should be highlighted when displaying the game
        board in the console. This cell is represented by a tuple of integers `(x, y)` where `x`
        is the column index and `y` is the row index
        """
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
                    print(f"|[{Color.BOLD}{self.grid[y][x].color}0{Color.RESET}]", end='')
                
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
                                print(f"|[{Color.BOLD}{conn.color}X{Color.RESET}]", end='')
                            elif conn.is_completed:
                                print(f"| {Color.BOLD}{conn.color}x{Color.RESET} ", end='')    
                            else:
                                print(f"| {conn.color}x{Color.RESET} ", end='')
                            break
                
                elif self.grid[y][x] == "#":
                    print("| # ", end='')
                
                else:
                    print("|   ", end='')
            
            print("|")
            print(f"{'-'* (self.columns* 4)}-")        

        if percentage == 100: print(f"{Color.GREEN}¡Felicidades! Has completado el nivel.{Color.RESET}") 
    
    def get_state(self):
        """
        The function `get_state` creates a board representation based on the grid and connections
        provided.
        :return: The `get_state` method returns a representation of the current state of the game board.
        It creates a new board structure based on the existing grid and connections in the game. The
        returned board contains information about the connections and their names, as well as the grid
        elements.
        
        Color names in uppercase are the color endpoints (circles).
        Lowercase names are parts of a color's path.
        
        ej
        ['BLUE', 'blue', '.', '.', 'YELLOW']
        ['GREEN', 'blue', 'YELLOW', 'GREEN', '.']
        ['.', 'blue', '.', 'BLUE', '.']
        ['.', '.', '.', '.', '.']
        ['RED', '.', '.', '.', 'RED']]
        """
        board = [[] for _ in range(self.rows)]
        
        for y in range(self.rows):
            for x in range(self.columns):

                if isinstance(self.grid[y][x], Connection):
                    board[y].append(self.grid[y][x].name.upper())
                elif (x, y) in [point for conn in self.connections for point in conn.road]:
                    for conn in self.connections:
                        if (x, y) in conn.road:
                            # Celda llena que es parte de una conexión
                                board[y].append(conn.name)
                else:
                    board[y].append(self.grid[y][x])
        return board
            
class FlowFree:
       
    def __init__(self, board:Board=None) -> None:
        self.board = board
        self.last_color_position = None
        self.last_move = None
        self.load_list_levels()
        self.level = None
    
    def load_list_levels(self) -> None:
        """
        The function `load_list_levels` categorizes level files based on their difficulty and extracts
        relevant information from the file names.
        Difficulty is determined by the board size:
        - Easy: boards up to 5x5
        - Medium: boards up to 9x9
        - Hard: larger boards
        ---------------
        
        In addition to saving a list of level names in the format:
        
        - "Nivel {number} - Tablero {size}, {number of colors} colores"
        
        Example: "Nivel 1 - Tablero 5x5, 4 colores"
        
        ---------------
        """
        
        
        levels_files = {"easy": [], "medium": [], "hard": []}
        levels_files_names = {"easy": [], "medium": [], "hard": []}
        for file in os.listdir("levels"):
            if file.endswith(".txt"):
                
                board, colors, level_number = file.replace(".txt", "").replace("_", " ").split()
                row, columns = board.split("x")
                # The code is determining the level of difficulty based on the product of the values
                # in the variables `row` and `columns`. If the product is less than or equal to 25,
                # the level is set to "easy". If the product is greater than 25 but less than or equal
                # to 81, the level is set to "medium". Otherwise, the level is set to "hard".
                if int(row) * int(columns) <= 25: level = "easy"
                elif int(row) * int(columns) <= 81: level = "medium"
                else: level = "hard"

                # The code snippet is appending a file to a list stored in the `levels_files`
                # dictionary at the key `level`, and appending a formatted string to a list stored in
                # the `levels_files_names` dictionary at the key `level`. The formatted string
                # includes the level number, board number, and quantity of colors.
                levels_files[level].append(file)
                levels_files_names[level].append(f"Nivel {level_number} - Tablero {board}, {colors[:-1]} colores")
        
        self.levels_files = levels_files
        self.levels_files_names = levels_files_names
     
    
    
        
    def app(self) -> None:
        """
        Presents a menu to the player to either play a game or exit, then proceeds to
        select a game level and play the game.
        
        :param player: Represent the player who is currently playing the game. Human or algorithm
        :return: The `app` method is returning `None`.
        """
        player = None
        while not self.board:
            options = ["Jugar", "Seleccionar Jugador", "Salir"]
            menu = Menu(options, "Flow Free")
            choice = menu.select()
            if options[choice] == "Salir":
                print("Saliendo del juego...")
                return
            elif options[choice] == "Seleccionar Jugador":
                player = self.select_player()
                if not player:
                    continue
                print(f"Jugador seleccionado: {player.name}")
                print("Presiona Enter para continuar")
                Control.select({'ENTER':None})
                continue
                
            self.select_level()
            
            if not self.board:
                continue
            if not player:
                player = HumanPlayer()
            if not player:
                self.board = None
                continue
            
            self.play(player=player)
            self.board = None
            print('Presiona Enter para salir')
            Control.select({'ENTER':None})
    
    def select_player(self) -> any:
        """
        Presents a menu to select a player type (Human or Algorithm) and returns the selected player instance.
        
        :return: The `select_player` method is returning an instance of `HumanPlayer`, `DFSPlayer`, `BFSPlayer`, or
        `AStarPlayer` classes, based on the user's selection from the menu. If the user selects "Volver", the method returns
        `None`.
        """
        from algorithms.astar import AStarPlayer as AStar
        from algorithms.bfs import BFSPlayer as BFS
        from algorithms.dfs import DFSPlayer as DFS
        options = ["Humano", "DFS", "BFS", "A*", "Volver"]
        menu = Menu(options, "Flow Free - Seleccionar jugador")
        choice = menu.select()
        
        if options[choice] == "Humano":
            return HumanPlayer()
        elif options[choice] == "DFS":
            return DFS()
        elif options[choice] == "BFS":
            return BFS()
        elif options[choice] == "A*":
            return AStar()
        else:
            return None
    
    def create_level_name(self, player) -> None:
        """
        Creates a level name based on the board's dimensions and number of colors.
        :return: The `create_level_name` method is returning a string that represents the level name.
        The level name is created by combining the number of rows, number of columns, and number of
        colors in the format "{rows}x{columns}_{colors}C.txt".
        """
        player_name = player.name
        number = 1
        name_files = self.level.replace(".txt", "")
        level_name = f"{player_name}_{name_files}-test_{number}.txt"
        ruta = os.path.join("output", level_name)
        
        while os.path.exists(ruta):
            level_name = f"{player_name}_{name_files}-test_{number}.txt"
            ruta = os.path.join("output", level_name)
            number += 1
        
        return level_name
    
    def select_level(self) -> None:
        """
        Allows the user to choose a level from levels folder and loads the selected level onto the game board.
        :return: If the user selects "Volver" in the first menu, the function will return without doing
        anything else. If the user selects a level and then selects "Volver" in the second menu, the
        function will also return without doing anything else. If the user selects a specific level and
        a file in the second menu, the function will set the board attribute of the object to a new
        FlowFreeBoard.
        """
        options =  [level.capitalize() for level, values in self.levels_files.items() if values]
        options.append("Volver")
        menu = Menu(options, "Flow Free - Seleccionar nivel")
        choice = menu.select()
        if options[choice] == "Volver":
            return
        
        level = options[choice].lower()
        files = self.levels_files[level]
        name_files = self.levels_files_names[level]
        name_files.append("Volver")
        menu = Menu(name_files, "Flow Free - Seleccionar nivel")
        
        choice = menu.select()
        
        name_files.pop()
        if choice == len(files):
            return
            
        file = files[choice]
        self.board = FlowFreeBoard(os.path.join("levels", file))
        self.level = file
        
        #MODIFICADO
    def play(self, player) -> None:
        is_human_player = isinstance(player, HumanPlayer)

        while True:
            
            percentage = self.board.percentage_filled()
            
            if percentage == 100:
                if not is_human_player:
                    level_name = self.create_level_name(player)
                    player._generate_reports(self.board, level_name=level_name)
                self.board.show()
                break
            
            # Show the board before the AI plays its turn to see the progress
            if not is_human_player:
                self.board.show()
                time.sleep(0.1) # Small delay to visualize the AI's progress
                
            move = player.play(self.board)
            
            if not move:
                print("Juego terminado.")
                break
            
            #If the player is not a human player, skip the rest of the loop and continue to the next iteration
            if not is_human_player:
                continue

            x, y = move    
            
            # If the cell is not valid, the code will skip to the
            # next iteration using the `continue` statement, without making any changes to the board.
            if not self.board._validate_cell(x, y):
                continue
            
            # if the cell is equal to the last move done by user, the player`s position will marked as None for select a new cell of out
            elif move == self.last_move:
                # The code snippet is checking if the variable `move` is equal to
                # `self.last_color_position`. If they are equal, it then calls the `pop_road()` method
                # on the grid element at position `y_color` and `x_color`, it will delete the current color of the color`s path.
                if move == self.last_color_position:
                    self.board.grid[y_color][x_color].pop_road()
                self.last_move = None
                self.last_color_position = None
                player.position = None
                continue
            
            # If player moves to the circle he has begined, the move is marked as None for delete the X to the path
            elif self.last_color_position and move == self.last_color_position:
                x_color, y_color = self.last_color_position
                self.board.grid[y_color][x_color].pop_road()
                self.last_move = move
                player.position = move
                continue
            
            # When player selects a new begin position
            elif not self.last_color_position:
                # If it is a circle point the road will be cleaned and the point will be added to the road.
                if isinstance(self.board.grid[y][x], Connection):
                    self.last_color_position = (x, y)
                    self.board.grid[y][x].clean_road()
                    self.board.grid[y][x].add_to_road(move)
                    
                # If player select a X point for begin, the last_color_position will be the color where point is
                else:
                    for conn in self.board.connections:
                        if (x, y) in conn.road:
                            self.last_color_position = conn.road[0]
                            break
                player.position = move
                continue
            
            # If the player has selected a color and try connect to a circle point, first verify if it circle is the
            # same color, if not, the board will not change
            elif isinstance(self.board.grid[y][x], Connection):
                x_color, y_color = self.last_color_position
                if self.board.grid[y][x].name != self.board.grid[y_color][x_color].name:
                    continue # Not same color
                
                # If it is the same color, the road is completed, and send to player to select another color/path
                self.board.grid[y][x].add_to_road(move)
                self.board.grid[y][x].check_completion()
                self.last_color_position = None
                player.position = None
                # Flow free move increase 1
                self.board.flow_free_moves += 1
                continue

            
            # The code snippet is checking if the tuple (x, y) is present in any of the road
            # connections in the self.board. If it is found in a connection, it breaks the road
            # connection at that point by calling the `break_road` method on that connection.
            elif (x, y) in [point for conn in self.board.connections for point in conn.road]:
                for conn in self.board.connections:
                    if (x, y) in conn.road:
                        conn.break_road((x, y))
                        break
            
            
                
            # The code snippet is setting the position of a player to a new move. It then retrieves
            # the last color position of the player and assigns it to `x_color` and `y_color`
            # variables. The `last_move` attribute of the player is updated with the new move.
            # Finally, the `add_to_road` method is called on the last_color_position grid on the board
            # with the new move as an argument.
            player.position = move
            x_color, y_color = self.last_color_position
            self.last_move = move
            self.board.grid[y_color][x_color].add_to_road(move)
    
    def algorithms_test(self, player, board) -> None:
        self.board = board

        while True:
            percentage = self.board.percentage_filled()
            if percentage == 100:
                level_name = self.create_level_name(player)
                player._generate_reports(self.board, level_name=level_name)
                break
            
            player.play(self.board)
            
# --- IGNORE ---
if __name__ == '__main__':
    board = FlowFreeBoard("levels/5x5_4C_1.txt")
    board.show()