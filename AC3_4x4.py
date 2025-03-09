import time
from collections import deque
from itertools import permutations

class AC3_4x4:
    def __init__(self, n, regions):
        self.n = n
        self.grid = [[0] * n for _ in range(n)]
        self.domains = [[set(range(1, n + 1)) for _ in range(n)] for _ in range(n)]
        self.regions = regions
        
        self.ac3_time = 0
        self.backtrack_time = 0
        self.total_solve_time = 0
    
    def solve(self):
        start_time = time.time()
        
        ac3_start = time.time()
        if not self.run_ac3():
            return False
        self.ac3_time = (time.time() - ac3_start) * 1000
        
        backtrack_start = time.time()
        solved = self.backtrack(0, 0)
        self.backtrack_time = (time.time() - backtrack_start) * 1000
        
        self.total_solve_time = (time.time() - start_time) * 1000
        
        return solved
    
    def run_ac3(self):
        queue = deque()
        
        for row in range(self.n):
            for col in range(self.n):
                self.add_row_column_arcs(queue, row, col)
                self.add_regions_arcs(queue, row, col)
        
        while queue:
            row1, col1, row2, col2 = queue.popleft()
            if self.revise(row1, col1, row2, col2):
                if not self.domains[row1][col1]:
                    return False
                self.add_row_column_arcs(queue, row1, col1)
                self.add_regions_arcs(queue, row1, col1)
        return True
    
    def add_row_column_arcs(self, queue, row, col):
        for i in range(self.n):
            if i != col:
                queue.append((row, col, row, i))
            if i != row:
                queue.append((row, col, i, col))
    
    def add_regions_arcs(self, queue, row, col):
        for region in self.regions:
            for cell in region['cells']:
                if cell == (row, col):
                    for other_cell in region['cells']:
                        if other_cell != cell:
                            queue.append((row, col, other_cell[0], other_cell[1]))
    
    def revise(self, row1, col1, row2, col2):
        revised = False
        to_remove = set()
        
        for val1 in self.domains[row1][col1]:
            if all(val1 == val2 for val2 in self.domains[row2][col2]):
                to_remove.add(val1)
                revised = True
        
        self.domains[row1][col1] -= to_remove
        return revised
    
    def backtrack(self, row, col):
        if row == self.n:
            return self.validate_regions()
        
        next_row, next_col = (row + 1, 0) if col == self.n - 1 else (row, col + 1)
        
        for value in sorted(self.domains[row][col]):
            if self.is_valid_assignment(row, col, value):
                self.grid[row][col] = value
                if self.backtrack(next_row, next_col):
                    return True
                self.grid[row][col] = 0
        
        return False
    
    def is_valid_assignment(self, row, col, value):
        return all(self.grid[row][i] != value for i in range(self.n)) and \
    all(self.grid[i][col] != value for i in range(self.n))
    
    def validate_regions(self):
        for region in self.regions:
            values = [self.grid[row][col] for row, col in region['cells']]
            if 0 in values:
                return False
            if not self.check_region_constraint(values, region['operation'], region['target']):
                return False
        return True
    
    def check_region_constraint(self, values, operation, target):
        if operation == '+':
            return sum(values) == target
        elif operation == '*':
            result = 1
            for v in values:
                result *= v
            return result == target
        elif operation == '-':
            return any(abs(a - b) == target for a, b in permutations(values, 2))
        elif operation == '/':
            return any(max(a, b) / min(a, b) == target for a, b in permutations(values, 2) if min(a, b) != 0)
        return False
    
    def print_grid(self):
        for row in self.grid:
            print(row)
    
    def print_performance_metrics(self):
        print("\nPerformance Metrics:")
        print(f"AC-3 Algorithm Time: {self.ac3_time:.3f} ms")

# Example cages for a 4x4 KenKen puzzle
regions = [
    {"cells": [(0, 0), (0, 1), (1, 0)], "operation": '*', "target": 24},
    {"cells": [(0, 2), (0, 3)], "operation": '/', "target": 2},
    {"cells": [(1, 1), (1, 2)], "operation": '-', "target": 3},
    {"cells": [(1, 3), (2, 3)], "operation": '-', "target": 1},
    {"cells": [(2, 0), (2, 1)], "operation": '+', "target": 5},
    {"cells": [(2, 2), (3, 2), (3, 3)], "operation": '+', "target": 6},
    {"cells": [(3, 0), (3, 1)], "operation": '-', "target": 3},
]

# Solve the puzzle
solver = AC3_4x4(4, regions)
if solver.solve():
    solver.print_grid()
    solver.print_performance_metrics()
else:
    print("No solution found.")
