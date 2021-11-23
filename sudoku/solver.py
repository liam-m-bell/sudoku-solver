import numpy as np
import copy
import time
import operator

class SudokuState:
    def __init__(self, grid):
        self.grid = grid
        
    def is_goal(self):
        for row in self.grid:
            for square in row:
                if square == 0:
                    return False
        return True            
    
    def is_valid(self):
        return self.check_sums(False)
    
    def get_final_state(self):
        pass
    
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
    
    def check_sums(self, checkingForGoal):
        if checkingForGoal:
            operation = operator.ne
        else:
            operation = operator.gt
        
        for row in self.grid:
            sum = 0
            for square in row:
                sum += square
            if operation(sum, 45):
                return False
        
        for row in self.grid.transpose():
            sum = 0
            for square in row:
                sum += square
            if operation(sum, 45):
                return False
            
        for i in range(3):
            for j in range(3):
                sum = 0
                for a in range(3 * i, i + 3, 1):
                    for b in range(3 * j, j + 3, 1):
                        sum += self.grid[a, b]     
                if operation(sum, 45):
                    return False
                
        return True

class SudokuSolver:
    def __init__(self):
        self.solution_found = False
        self.solution = np.full([9, 9], -1)
    
    def solve(self, sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku.grid[i, j] == 0:
                    for n in range(1, 10, 1):
                        if sudoku.check_valid_move(i, j, n):
                            sudoku.grid[i, j] = n
                            self.solve(sudoku)
                            sudoku.grid[i, j] = 0
                            
                    return self.solution
        
        if not self.solution_found:        
            self.solution = np.copy(sudoku.grid)
            self.solution_found = True
        


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
    solver = SudokuSolver()
    print(sudoku)
    solved_sudoku = solver.solve(SudokuState(sudoku))
    
    return solved_sudoku

sudokus = np.load(f"data/hard_puzzle.npy")
solutions = np.load(f"data/hard_solution.npy")
for i in range(len(sudokus)): 
    start = time.perf_counter()
    print(sudoku_solver(sudokus[i]))
    end = time.perf_counter()
    print(solutions[i])
    print(end - start)
    print("\n\n")