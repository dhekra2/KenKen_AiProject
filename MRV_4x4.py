import itertools
import time

class MRV_4x4:
    def __init__(self, size, regions):
        self.N = size
        self.grid = [[0] * size for _ in range(size)]
        self.domains = [[set(range(1, size + 1)) for _ in range(size)] for _ in range(size)]
        self.regions = regions
        self.execution_time = 0
    
    def is_valid_assignment(self, row, col, value):
        
        for i in range(self.N):
            if self.grid[row][i] == value or self.grid[i][col] == value:
                return False
        return True
    
    def validate_regions(self):
        for cells, operation, target in self.regions:
            values = [self.grid[r][c] for r, c in cells]
            if 0 in values:
                continue  
            if not self.check_region_constraint(values, operation, target):
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
            return abs(values[0] - values[1]) == target
        elif operation == '/':
            return max(values) / min(values) == target
        return False
    
    def solve(self):
        start_time = time.time()
        result = self.backtrack()
        self.execution_time = (time.time() - start_time) * 1000  
        return result
    
    def backtrack(self):
        # Find next unassigned cell using MRV heuristic
        row, col = self.select_mrv_variable()
        if row == -1:
            return True  # Solution found
        
        for value in sorted(self.domains[row][col]):
            if self.is_valid_assignment(row, col, value):
                self.grid[row][col] = value
                if self.validate_regions():
                    if self.backtrack():
                        return True
                self.grid[row][col] = 0
        
        return False
    
    def select_mrv_variable(self):
        min_remaining_values = float('inf')
        selected_var = (-1, -1)
        
        for row in range(self.N):
            for col in range(self.N):
                if self.grid[row][col] == 0:
                    remaining_values = len(self.domains[row][col])
                    if remaining_values < min_remaining_values:
                        min_remaining_values = remaining_values
                        selected_var = (row, col)
        
        return selected_var
    
    def print_grid(self):
        for row in self.grid:
            print(row)
    
    def print_execution_time(self):
        print(f"Execution Time: {self.execution_time:.3f} ms")

if __name__ == "__main__":
    regions = [
        ([(0, 0), (0, 1), (1, 0)], '*', 24),
        ([(0, 2), (0, 3)], '/', 2),
        ([(1, 1), (1, 2)], '-', 3),
        ([(1, 3), (2, 3)], '-', 1),
        ([(2, 0), (2, 1)], '+', 5),
        ([(2, 2), (3, 2), (3, 3)], '+', 6),
        ([(3, 0), (3, 1)], '-', 3)
    ]
    solver = MRV_4x4(4, regions)
    if solver.solve():
        solver.print_grid()
        solver.print_execution_time()
    else:
        print("No solution found.")
