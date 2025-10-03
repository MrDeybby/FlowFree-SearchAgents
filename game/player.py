from control import Control
from color import Color
from flow_free import FlowFreeBoard, FlowFree

class Player:
    
    def play(self):
        pass
    
# [['red', 'green', 'red', 'blue', 'yellow', '.', 'yellow'], 
# ['.', '.', '.', '.', '.', '.', '.'], 
# ['.', '.', '.', '.', '.', '.', '.'], 
# ['.', '.', '#', '.', '.', '.', '.'], 
# ['.', '.', '.', '.', '.', '.', '.'], 
# ['.', 'green', '.', '.', '.', '.', '.'], 
# ['.', '.', '.', 'blue', '#', '.', '.']]

# class DFS(Player): 

class HumanPlayer(Player):
    
    BOARD_CONTROL = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0), 'ENTER': 'SELECT', 'ESC': 'QUIT'}
    NUMBER_SELECTION_CONTROL = {'A': -1, 'D': 1, 'ENTER': 'SELECT', 'ESC': 'QUIT'}
    SELECT_CONTROL = {'A': -1, 'D': 1, 'ENTER': 'SELECT', 'ESC': 'QUIT'}
    
    def __init__(self):
        self._current_cell = None
        
    @property
    def position(self):
        return self._current_cell
    
    @position.setter
    def position(self, value):
        self._current_cell = value
    
    def play(self, board:FlowFreeBoard) -> None:
        if not self._current_cell:
            current_cell = self._select_cell(board)          
            return current_cell
        else:
            x, y = self._current_cell
        
        board.show(highlight_cell=(x, y))
        move = Control.select(self.BOARD_CONTROL)
        
        if move == 'QUIT':
            return None
        elif move == 'SELECT':
            # Deselect current cell for choise another whith self._select_cell
            self._current_cell = None
            return (x, y)
        
        move_x, move_y = move
        current_cell = x + move_x, y + move_y
        return (current_cell)
        
        
    @classmethod
    def _select_cell(cls, board:FlowFreeBoard, current_index = 0) -> any:
        numbers_cells = board._get_selectable_cells()
        current_cell = numbers_cells[current_index]

        while True:
            board.show(current_cell) # Display the board
            print("Selecciona una salida")
            move = Control.select(cls.SELECT_CONTROL)
            
            if move == 'SELECT':
                return current_cell
            elif move == 'QUIT':
                return None
            
            # Move selection
            current_index += move
            if current_index < 0: current_index = len(numbers_cells) - 1
            elif current_index == len(numbers_cells): current_index = 0
            current_cell = numbers_cells[current_index]
                
                
            
            
if __name__ == "__main__":
    board = FlowFreeBoard("levels/5x5_4C_1.txt")
    game = FlowFree(board)
    player = HumanPlayer()
    game.play(player=player)    
        