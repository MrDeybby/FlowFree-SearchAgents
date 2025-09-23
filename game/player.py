from control import Control
from color import Color
from flow_free import Connection, FlowFreeBoard

class Player:
    
    def play(self):
        pass
    

class HumanPlayer(Player):
    
    BOARD_CONTROL = {'W': 'UP', 'A': 'LEFT', 'S': 'DOWN', 'D': 'RIGHT', 'ENTER': 'SELECT', 'ESC': 'QUIT'}
    NUMBER_SELECTION_CONTROL = {'A': -1, 'D': 1, 'ENTER': 'SELECT', 'ESC': 'QUIT'}
    
    @classmethod    
    def play(cls, board:FlowFreeBoard) -> None:
        board.show() # Display the board
        move = Control.select(cls.BOARD_CONTROL)
    
    @staticmethod
    def _select_cell(board:FlowFreeBoard) -> None:
        numbers_cells = HumanPlayer._numbers_cells(board)
        current_index = 0
        current_cell = numbers_cells[current_index]
        
        while True:
            print(f"{'-'* (board.columns * 4)}-")
            
            
            for y in range(board.rows):
                for x in range(board.columns):
                    
                    # Highlight current cell
                    if (x, y) == current_cell and isinstance(board.grid[y][x], Connection):
                        print(f"| {Color.BOLD}{board.grid[y][x].color}0{Color.RESET} ", end='')
                        
                    elif (x, y) == current_cell and isinstance(board.grid[y][x], Connection):
                        print(f"| {Color.BACKGROUND_GRAY}{board.grid[y][x].color}O{Color.RESET} ", end='') 
                        
                    elif isinstance(board.grid[y][x], Connection):
                        print(f"| {board.grid[y][x].color}O{Color.RESET} ", end='')
                    elif board.grid[y][x] is None:
                        print("| X ", end='')
                    elif board.grid[y][x] == '.':
                        print("|   ", end='')
                        
                print("|")
                print(f"{'-'* (board.columns* 4)}-")  
                
            move = Control.select(HumanPlayer.NUMBER_SELECTION_CONTROL)
            if isinstance(move, int):
                current_index += move
                if current_index < 0: current_index = len(numbers_cells) - 1
                elif current_index == len(numbers_cells): current_index = 0
                current_cell = numbers_cells[current_index]
                # continue
            
            elif move == 'SELECT':
                return current_cell
            elif move == 'QUIT':
                return None        
        
    @staticmethod
    def _numbers_cells(board:FlowFreeBoard) -> list[tuple[int, int]]:
        cells = []
        for r in range(board.rows):
            for c in range(board.columns):
                if isinstance(board.grid[r][c], Connection):
                    cells.append((c, r))
        return cells
        
        
if __name__ == "__main__":
    board = FlowFreeBoard("levels/5_x_5_4C_1.txt")
    HumanPlayer._select_cell(board)
        
        