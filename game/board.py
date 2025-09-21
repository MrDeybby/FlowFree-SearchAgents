class Board:
    
    def __init__(self, rows:int, cols:int) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.length = rows * cols
        