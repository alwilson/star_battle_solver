#!/usr/bin/env python3

import z3
import pprint as pp

# Easy A
# puzzle = [[0, 0, 0, 0, 0, 0, 1, 1, 2],
#           [0, 0, 0, 3, 3, 3, 1, 1, 2],    
#           [4, 4, 3, 3, 5, 3, 3, 1, 2],
#           [4, 4, 3, 5, 5, 5, 3, 2, 2],    
#           [6, 4, 3, 3, 3, 3, 3, 2, 2],
#           [6, 6, 3, 7, 7, 8, 3, 2, 2],
#           [6, 6, 3, 7, 7, 8, 3, 2, 2],
#           [6, 6, 3, 7, 7, 8, 3, 2, 2],    
#           [6, 6, 6, 8, 8, 8, 8, 8, 8]]

# Random Ludicrous
# www.starbattleinfinity.com/play/992W2ZR9aoU4B0L0Yjw_OxDrga89~Star%02Battle%02∞%02Challenge~9x9%02/%02Ludicrous%02/%02CasGen
puzzle = [[0, 0, 0, 0, 0, 1, 1, 2, 2],
          [1, 1, 1, 0, 1, 1, 4, 2, 2],    
          [1, 5, 1, 1, 1, 4, 4, 4, 2],
          [1, 5, 5, 5, 6, 6, 6, 4, 2],    
          [1, 1, 1, 5, 5, 5, 6, 4, 2],
          [7, 5, 5, 5, 5, 5, 4, 4, 4],
          [7, 7, 7, 5, 5, 3, 4, 4, 4],
          [3, 3, 3, 3, 3, 3, 8, 8, 4],    
          [3, 3, 8, 8, 8, 8, 8, 8, 8]]

width = len(puzzle[0])
height = len(puzzle)

pp.pprint(puzzle)

# Debug stuff to help print out *most* the constraints
num = 20000
z3.set_option(max_args=num, max_lines=num, max_depth=num, max_visited=num)

solver = z3.Solver()

# Create a 2D array of Z3 integer variables
grid = [[z3.Int("grid_%s_%s" % (i, j)) for j in range(width)] for i in range(height)]

for wi in range(width):
    for hi in range(height):
        # Each cell must be between 1 and 9
        cell = grid[hi][wi]
        cell_constraint = z3.Or(cell == 0, cell == 1)

        # Add the constraints to the solver
        solver.add(cell_constraint)

for wi in range(width):
    # Each column must sum to the value 2
    column_sum = z3.Sum([grid[hi][wi] for hi in range(height)])
    column_constraint = z3.Or(column_sum == 2)

    # Add the constraints to the solver
    solver.add(column_constraint)

for hi in range(height):
    # Each row must sum to the value 2
    row_sum = z3.Sum([grid[hi][wi] for wi in range(width)])
    row_constraint = z3.Or(row_sum == 2)

    # Add the constraints to the solver
    solver.add(row_constraint)


# For each region in grid restrict the sum of the cells to 2
for ri in range(9):
    region_sum = 0
    for wi in range(width):
        for hi in range(height):
            if puzzle[hi][wi] == ri:
                region_sum += grid[hi][wi]

    # Add the constraints to the solver
    solver.add(region_sum == 2)

for wi in range(width):
    for hi in range(height):
        cell = grid[hi][wi]
        # For each cell set to 1 all neighboring cells must be 0
        if wi > 0:
            cell_constraint = z3.Or(cell == 0, grid[hi][wi - 1] == 0)
            solver.add(cell_constraint)
        if wi < width - 1:
            cell_constraint = z3.Or(cell == 0, grid[hi][wi + 1] == 0)
            solver.add(cell_constraint)
        if hi > 0:
            cell_constraint = z3.Or(cell == 0, grid[hi - 1][wi] == 0)
            solver.add(cell_constraint)
        if hi < height - 1:
            cell_constraint = z3.Or(cell == 0, grid[hi + 1][wi] == 0)
            solver.add(cell_constraint)
        # All diagonal cells must be 0 as well
        if wi > 0 and hi > 0:
            cell_constraint = z3.Or(cell == 0, grid[hi - 1][wi - 1] == 0)
            solver.add(cell_constraint)
        if wi < width - 1 and hi > 0:
            cell_constraint = z3.Or(cell == 0, grid[hi - 1][wi + 1] == 0)
            solver.add(cell_constraint)
        if wi > 0 and hi < height - 1:
            cell_constraint = z3.Or(cell == 0, grid[hi + 1][wi - 1] == 0)
            solver.add(cell_constraint)
        if wi < width - 1 and hi < height - 1:
            cell_constraint = z3.Or(cell == 0, grid[hi + 1][wi + 1] == 0)
            solver.add(cell_constraint)

# Print out the constraints if needed
# print(solver.assertions())

ret = solver.check()
if ret == z3.sat:
    model = solver.model()
    for hi in range(height):
        for wi in range(width):
            cell = grid[hi][wi]
            print(model[cell], end=" ")
        print()
else:  
    print("Failed to solve puzzle")
