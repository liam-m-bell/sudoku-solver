import numpy as np
import copy
import time
import operator

class SudokuState:
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
        '''for row in self.grid:
            for square in row:
                if square == 0:
                    return False
        return True          ''' 
        for row in self.possible_values:
            for cell_values in row:
                if len(cell_values) != 1:
                    return False
        return True
    
    def is_valid(self):
        for i in range(9):
            for j in range(9):
                if len(self.possible_values[i, j]) == 0:
                    return False
        return True
        
    def get_possible_values(self, x, y):
        return copy.copy(self.possible_values[x, y])
    
    def get_initial_possible_values(self, x, y):
        if (self.grid[x, y] != 0):
            return {self.grid[x, y]}
        else: 
            return {1, 2, 3, 4, 5, 6, 7, 8, 9} - self.get_related_values(x, y) - {0}
    
    def get_row_values(self, y):
        return set(np.transpose(self.grid)[y])
    
    def get_column_values(self, x):
        return set(self.grid[x])
    
    def get_box_values(self, x, y):
        values = set()
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                values.add(self.grid[i,j])
                
        return values
    
    def get_related_values(self, x, y):
        return self.get_row_values(y).union(self.get_column_values(x)).union(self.get_box_values(x, y))
    
    def get_related_possible_values(self, x, y):
        values = set()
        for i in range(9):
            values.union(self.get_possible_values(x, i))
            values.union(self.get_possible_values(i, y))
            
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                values.union(self.get_possible_values(i, j))
        
        return values
    
    def get_unfilled_cells(self):
        cells = set()
        for x in range(9):
            for y in range(9):
                if self.grid[x, y] == 0:
                    cells.add((x, y))
        return cells
    
    def get_singleton_cells(self):
        cells = set()
        for cell in self.get_unfilled_cells():
            if len(self.possible_values[cell[0], cell[1]]) == 1:
                cells.add(cell)              
        return cells
        
    def check_for_unique_values(self):
        for cell in self.get_unfilled_cells():
            x = cell[0]
            y = cell[1]
            for a in self.get_possible_values(x, y):
                is_unique = True
                for b in self.get_related_possible_values(x, y):
                    if a == b:
                        is_unique = False
                        break
                if is_unique:
                    self.set_value(x, y, a)
    
    def set_value(self, x, y, value):
        state = copy.deepcopy(self)
        
        state.possible_values[x, y] = {value}
        state.grid[x, y] = value
        
        
        # Update the grid
        # Row

        for i in range(9):
            if i != x:
                if value in state.possible_values[i, y]:
                    state.possible_values[i, y].remove(value)
        
        # Column
        for i in range(9):
            if i != y:
                if value in state.possible_values[x, i]:
                    state.possible_values[x, i].remove(value)
                
        # Box
        for i in range(3 * (x // 3), 3 * (x // 3) + 3, 1):
            for j in range(3 * (y // 3), 3 * (y // 3) + 3, 1):
                if not (i == x and j == y):
                    if value in state.possible_values[i, j]:
                        state.possible_values[i, j].remove(value)
            
        # Singleton cells     
        singleton_cells = list(state.get_singleton_cells())
        while len(singleton_cells) > 0:
            a = singleton_cells[0][0]
            b = singleton_cells[0][1]
            final_value = list(state.possible_values[a, b])[0]
            state = state.set_value(a, b, final_value)
            singleton_cells = state.get_singleton_cells()
        
            state.check_for_unique_values()
        
        return state
    
    
    def check_valid_move(self, x, y, value):
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
    
    def check_sums(self):
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
        

def pick_next_cell(sudoku : SudokuState):
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
    if sudoku.is_goal():
        return sudoku
    

    
    cell_index = pick_next_cell(sudoku)
    if cell_index is not None:
        values = sudoku.get_possible_values(cell_index[0], cell_index[1])
        
        for value in values:
            new_state = sudoku.set_value(cell_index[0], cell_index[1], value)
            if new_state.is_goal():
                return new_state
            if new_state.is_valid():
                deep_state = depth_first_search(new_state)
                if deep_state is not None and deep_state.is_goal():
                    return deep_state
            
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
            


if __name__ == "__main__":
    sudokus = np.load(f"data/medium_puzzle.npy")
    solutions = np.load(f"data/medium_solution.npy")
    print("\n\nHARD\n\n")
    for i in range(len(sudokus)):
        print(sudokus[i])
        start = time.perf_counter()
        result = sudoku_solver(sudokus[i])
        end = time.perf_counter()
        print(result)
        print(solutions[i])
        print(end - start)
        print("\n\n")
        
    ''' sudokus = np.load(f"data/hard_puzzle.npy")
    solutions = np.load(f"data/hard_solution.npy")
    start = time.perf_counter()
    for i in range(len(sudokus)):
        sudoku_solver(sudokus[i])    
    end = time.perf_counter()
    print(end - start)'''
        