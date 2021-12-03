from typing import Set
import numpy as np
import copy

class SudokuState:
    """A state of a partially completed Sudoku puzzle.
    """    
    def __init__(self, grid):
        self.failed = False
        self.grid = grid
        self.possible_values = np.array([set() for i in range(81)]).reshape(9, 9)
        for x in range(9):
            for y in range(9):
                self.possible_values[x, y] = self.get_initial_possible_values(x, y)
                if len(self.possible_values[x, y]) == 1:
                    self.grid[x, y] = list(self.possible_values[x, y])[0]
        
    def is_goal(self):
        """State is a goal state if all cells have only one possible value.

        Returns:
            bool: Whether the state is a goal state.
        """
        for row in self.possible_values:
            for cell_values in row:
                if len(cell_values) != 1:
                    return False
        return True
    
    def is_valid(self):
        """State is valid if any cell has no possible value.

        Returns:
            bool: Whether the state is valid.
        """             
        for i in range(9):
            for j in range(9):
                if len(self.possible_values[i, j]) == 0:
                    return False
        return True
        
    def get_possible_values(self, x, y):
        """Gets the possible values for a particular cell.

        Args:
            x (int): The row index.
            y (int): The column index.

        Returns:
            set: The set of the possible values that the cell could take.
        """             
        return copy.copy(self.possible_values[x, y])
    
    def get_initial_possible_values(self, x, y):
        """Generates the initial possible values for a cell.

        Args:
            x (int): The row index.
            y (int): The collumn index.

        Returns:
            set: The set of the possible values that the cell could take.
        """        
        if (self.grid[x, y] != 0):
            return {self.grid[x, y]}
        else: 
            return {1, 2, 3, 4, 5, 6, 7, 8, 9} - self.get_related_values(x, y) - {0}
    
    def get_row_values(self, x):
        """Gets the values which are contained within a row.

        Args:
            x (int): The row index.

        Returns:
            set: The set of values in the row.
        """        
        return set(np.transpose(self.grid)[x])
    
    def get_column_values(self, y):
        """Gets the values which are contained within a column.

        Args:
            y (int): The column index.

        Returns:
            set: The set of values in the column.
        """        
        return set(self.grid[y])
    
    def get_box_values(self, x, y):
        """Gets the values which are contained within a box.

        Args:
            x (int): The row index of a cell within the box.
            y (int): The column index of a cell within the box.

        Returns:
            set: The set of values in the box.
        """        
        values = set()
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                values.add(self.grid[i,j])
                
        return values
    
    def get_related_values(self, x, y):
        """Get the values which are in the same row, column or box as a particular cell.

        Args:
            x (int): The row index.
            y (int): The column index

        Returns:
            set: The union of the values in the same row, column and box.
        """             
        return self.get_row_values(y).union(self.get_column_values(x)).union(self.get_box_values(x, y))
    
    # UNUSED
    def get_related_possible_values(self, x, y):
        """Gets the union of all the possible values of all other cells in the same row, column or box as a particular cell.

        Args:
            x (int): The row index.
            y (int): The column index.

        Returns:
            set: The union of all the possible values of all other cells in the same row, column or box as a particular cell.
        """        
        values = set()
        for i in range(9):
            if i != x:
                values = values.union(self.get_possible_values(x, i))
            if i != y:
                values = values.union(self.get_possible_values(i, y))
            
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                if i != x and j != y:
                    values = values.union(self.get_possible_values(i, j))
        
        return values
    
    def get_unfilled_cells(self):
        """Gets the cells in the grid which have not been assinged a value.

        Returns:
            set: The set of unassinged cells.
        """        
        cells = set()
        for x in range(9):
            for y in range(9):
                if self.grid[x, y] == 0:
                    cells.add((x, y))
        return cells
    
    def get_singleton_cells(self):
        """Gets the unassinged cells in the grid which have only one possible value.

        Returns:
            set: The set of singleton cells.
        """        
        cells = set()
        for cell in self.get_unfilled_cells():
            if len(self.possible_values[cell[0], cell[1]]) == 1:
                cells.add(cell)              
        return cells
    
    # UNUSED
    def check_for_unique_values(self, cell):
        """Checks if a cell has a possible value which is unique within the union of the possible values of its related cells.

        Args:
            cell ((int, int)): The index of the cell.
        """        
        x = cell[0]
        y = cell[1]
        for a in self.get_possible_values(x, y):
            if not (a in self.get_related_possible_values(x, y)):
                self.set_value(x, y, a)
    
    def set_value(self, x, y, value):
        """Gets a new state which has had a value assinged to a cell with the constraint propagated.

        Args:
            x (int): The row index.
            y (int): The column index.
            value (int): The value to set.

        Returns:
            SudokuState: The new state.
        """
        
        # Create copy of state
        state = copy.deepcopy(self)
        
        state.possible_values[x, y] = {value}
        state.grid[x, y] = value      
        
        # Propagate the constraints by updating the possible values of the related cells.

        # Row
        for i in range(9):
            if i != y:
                if value in state.possible_values[x, i]:
                    state.possible_values[x, i].remove(value)

        # Column
        for i in range(9):
            if i != x:
                if value in state.possible_values[i, y]:
                    state.possible_values[i, y].remove(value)
                
        # Box
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                if not (i == x and j == y):
                    if value in state.possible_values[i, j]:
                        state.possible_values[i, j].remove(value)
            
        # Assign values to singleton cells (cells with only one possible value)
        singleton_cells = list(state.get_singleton_cells())
        while len(singleton_cells) > 0:
            a = singleton_cells[0][0]
            b = singleton_cells[0][1]
            final_value = list(state.possible_values[a, b])[0]
            state = state.set_value(a, b, final_value)
        return state
    
    def check_sums(self):
        """Checks if a completed sudoku is a legal solution by checking the sums of the rows, columns and boxes add to 45.

        Returns:
            bool: Whether the sudoku is a solution.
        """        
        for row in self.grid:
            sum = 0
            for square in row:
                sum += square
            if sum != 45:
                return False
        
        for row in self.grid.transpose():
            sum = 0
            for square in row:
                sum += square
            if sum != 45:
                return False
            
        for i in range(3):
            for j in range(3):
                sum = 0
                for a in range(3 * i, 3 * i + 3, 1):
                    for b in range(3 * j, 3 * j + 3, 1):
                        sum += self.grid[a, b]     
                if sum != 45:
                    return False
                
        return True
    
    # UNUSED
    def check_valid_move(self, x, y, value):
        """Checks if assinging a value to a cell is a vaild and legal move.

        Args:
            x (int): The row index.
            y (int): The column index.
            value (int): The value to try.

        Returns:
            bool: Whether the move is valid.
        """        
        for i in range(9):
            if self.grid[x][i] == value:
                return False
        for j in range(9):
            if self.grid[j][y] == value:
                return False
            
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                if self.grid[i, j] == value:
                    return False
                
        return True
        

def pick_next_cell(sudoku : SudokuState):
    """Gets the index of the next cell of a sudoku to use in the search.

    Args:
        sudoku (SudokuState): The state of the sudoku puzzle.

    Returns:
        (int, int): The index of the cell.
    """    
    cell_index = None
    for i in range(9):
        for j in range(9):
            if sudoku.grid[i, j] == 0 and len(sudoku.possible_values[i, j]) > 1:
                if cell_index is None:
                    cell_index = (i, j)
                elif len(sudoku.possible_values[i, j]) < len(sudoku.possible_values[cell_index[0], cell_index[1]]):
                    cell_index = (i, j)
    
    return cell_index           
         
def depth_first_search(sudoku : SudokuState):
    """Perform depth first search on a sudoku state, trying possible values for each cell.

    Args:
        sudoku (SudokuState): The state to use for the search.

    Returns:
        SudokuState: The resultant state from the search.
    """    
    if sudoku.is_goal():
        return sudoku

    cell_index = pick_next_cell(sudoku)
    if cell_index is not None:
        values = sudoku.get_possible_values(cell_index[0], cell_index[1])
        for value in values:
            state = sudoku.set_value(cell_index[0], cell_index[1], value)
            if state.is_goal():
                return state
            if state.is_valid():
                new_state = depth_first_search(state)
                if new_state is not None and new_state.is_goal():
                    return new_state
            
    return None

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    solved_sudoku = depth_first_search(SudokuState(sudoku))
    if solved_sudoku is None:
        return np.full([9, 9], -1)
    else:
        if solved_sudoku.check_sums():
            return solved_sudoku.grid
        else:
            return np.full([9, 9], -1)