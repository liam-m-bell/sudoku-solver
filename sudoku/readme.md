# Sudoku solver

This file explains the approach taken in the design of an agent which solves sudoku puzzles.

## Choice of algorithm

The algorithm used to solve the puzzles is a backtracking depth-first search with constraint satisfaction.

### Backtracking depth-first search

In the search an empty cell from the sudoku is chosen which has the fewest possible values which that cell can take.
Then for each of these possible values, the value of the cell is set to the value and is checked to see if this new state is the goal state (a completed sudoku puzzle) which means the search is complete.

If the new state is not the goal state however, then, granted that the state is not an invalid puzzle, the state is used recursively using the same depth-first search and is checked for whether the result from this search has resulting in a goal state. 

If the goal state is not found, then the sudoku is declared invalid (it has no possible solution).

This algorithm was chosen as it relatively simple to implement, although other approaches which use iteration rather than recursion may have performed better.

### Constraint satisfaction

Constraint satisfaction is implemented by, during the process of the setting of the value to create a new state, the possible values for all the related cells are updated accordingly; the value which is set is removed from the set of possible values of the other cells in the same row, column or box as the original cell.

Following this process, any cell in the sudoku grid which now only has one possible value it could take (referred to as singleton cells), is assigned the value of its only possible value, recursively using the set value method until there are no longer any singleton cells.

Further methods were considered for helping the search such as searching for unique possible values within the union of the row, column and box of a particular cell. This would determine that this value must be the value for that cell. However a attempted implementation of this heuristic did not seem to improve the efficiency of the search, so was not included in the final algorithm.

## Choice of data structures

A 'SudokuState' class was created to represent a sudoku puzzle.

The state contains a two-dimensional integer numpy array to store the values that each of the cells in the sudoku grid have been set to.

Another two-dimensional numpy array is also used to store the possible values that each of the cells in the grid could take. Each element in the array is a set which contains the possible values each cell with the corresponding index.
A set was used to store the possible values, as the values are an unordered collection and each element is unique.

A set of tuples is used to store the indices of the singleton cells. The set of added to when a cell's length of possible values becomes one.
To begin with a different approach of searching for singleton cells each time a new value was set, was used. However, this approach, on average, took over twice as long to solve most of the hard sudoku puzzles, compared to only updating a set of values only when a change was needed.

The encapsulation of this data in a class was very important so that states could be easily used in the search and set value functions which also utilise python's library which allows the deep copying of objects so that new states could be easily created.

