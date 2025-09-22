from control import Control
from color import Color
from flow_free import Connection, FlowFreeBoard
class Player:
    
    def play(self):
        pass
    

class HumanPlayer(Player):
    
    BOARD_CONTROL = {'W': 'UP', 'A': 'LEFT', 'S': 'DOWN', 'D': 'RIGHT', 'ENTER': 'SELECT', 'ESC': 'QUIT'}
    
    @classmethod    
    def play(cls, board:FlowFreeBoard) -> None:
        board.show()
        move = Control.select(cls.BOARD_CONTROL)
    
    @staticmethod
    def _select_cell(board:FlowFreeBoard) -> None:
        current_cell = (0, 0)
        print(f"{'-'* (board.columns * 4)}-")
        
        for y in range(board.rows):
            for x in range(board.columns):
                
                # Highlight current cell
                if (x, y) == current_cell and isinstance(board.grid[y][x], Connection):
                    print(f"| {Color.BACKGROUND_GRAY}{board.grid[y][x].color}O{Color.RESET} ", end='')
                    
                if (x, y) == current_cell and isinstance(board.grid[y][x], Connection):
                    print(f"| {Color.BACKGROUND_GRAY}{board.grid[y][x].color}O{Color.RESET} ", end='') 
                       
                elif isinstance(board.grid[y][x], Connection):
                    print(f"| {board.grid[y][x].color}O{Color.RESET} ", end='')
                elif board.grid[y][x] is None:
                    print("| X ", end='')
                elif board.grid[y][x] == '.':
                    print("|   ", end='')
                    
            print("|")
            print(f"{'-'* (board.columns* 4)}-")  
        pass
        
        
        
        
        