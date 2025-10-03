# The `Board` class represents a grid with specified rows and columns, providing methods to validate
# cell coordinates within the grid bounds.
class Board:
    
    def __init__(self, rows:int, columns:int) -> None:
        """
        The function initializes a grid with a specified number of rows and columns, filled with empty
        spaces.
        
        :param rows: The `rows` parameter in the `__init__` method represents the number of rows in a
        grid or matrix. It specifies how many horizontal lines or levels the grid will have
        :type rows: int
        :param columns: The `columns` parameter in the `__init__` method represents the number of
        columns in a grid. It is used to initialize the number of columns in the grid and to create 
        a 3D list with the specified number of columns for each row.
        :type columns: int
        """
        self.rows = rows
        self.columns = columns
        # The line `self.grid = [[' ' for _ in range(columns)] for _ in range(rows)]` in the
        # `__init__` method of the `Board` class is initializing a 3D list representing the grid with
        # the specified number of rows and columns.
        self.grid = [[' ' for _ in range(columns)] for _ in range(rows)]
        self.length = rows * columns
    
    
    def _validate_cell(self, x:int, y:int) -> bool:
        """
        The `_validate_cell` method checks if the given coordinates (x, y) are within the bounds of a
        grid. The `_validate_cell` method takes two parameters, `x` and `y`, which represent the
        coordinates of a cell in a grid.
        
        :param x: The parameter `x` represents the horizontal position or column index in a grid or matrix. In
        the context of the `_validate_cell` method, `x` is used to check if the given column index is within
        the valid range of column in the grid
        type x: int
        :param y: The parameter `y` represents the vertical position or row index in a grid or matrix. In
        the context of the `_validate_cell` method, `y` is used to check if the given row index is within
        the valid range of rows in the grid
        :return: The _validate_cell method returns a boolean value - True if the cell coordinates (x, y) are
        within the bounds of the grid (0 <= x < self.columns and 0 <= y < self.rows), and False otherwise.
        type y: int
        """
        
        # The code snippet `if not (0 <= x < self.columns) or (not 0 <= y < self.rows): return False
        # return True` is a conditional statement within the `_validate_cell` method of the `Board`
        # class in Python.
        if not (0 <= x < self.columns) or (not 0 <= y < self.rows):
            return False
        return True