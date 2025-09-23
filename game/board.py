class Board:
    
    def __init__(self, rows:int, columns:int) -> None:
        self.rows = rows
        self.columns = columns
        self.grid = [[' ' for _ in range(columns)] for _ in range(rows)]
        self.length = rows * columns
    
    
    def _validate_cell(self, x, y) -> bool:
        if not (0 <= x < self.columns) or (not 0 <= y < self.rows):
            return False
        return True