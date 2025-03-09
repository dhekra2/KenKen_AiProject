import time
from collections import deque

class region:
    def __init__(self, cells, operation, target):
        self.cells = cells
        self.operation = operation
        self.target = target

class CSP:
    def __init__(self, grid_size, regions):
        self.grid_size = grid_size
        self.regions = regions
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.domains = [[set(range(1, grid_size + 1)) for _ in range(grid_size)] for _ in range(grid_size)]
        self._initial_constraints()

    def _initial_constraints(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.domains[i][j] = self.filter_domain(i, j, self.domains[i][j])
        for cage in self.regions:
            self._region_constraint(cage)

    def filter_domain(self, row, col, domain):
        for i in range(self.grid_size):
            domain.discard(self.grid[row][i])
            domain.discard(self.grid[i][col])
        return domain

    def _region_constraint(self, region):
        for (x, y) in region.cells:
            self.domains[x][y] = self.filter_region_domain(x, y, region.operation, region.target, region.cells)

    def filter_region_domain(self, x, y, operation, target, cells):
        return {value for value in self.domains[x][y] if self.valid_region_value(x, y, value, operation, target, cells)}

    def valid_region_value(self, x, y, value, operation, target, cells):
        original_value = self.grid[x][y]
        self.grid[x][y] = value
        
        if operation == '+':
            result = self.check_sum(cells, target)
        elif operation == '-':
            result = self.check_difference(cells, target)
        elif operation == '*':
            result = self.check_product(cells, target)
        elif operation == '/':
            result = self.check_division(cells, target)
        else:
            result = True
        
        self.grid[x][y] = original_value
        return result

    def check_sum(self, cells, target):
        total = sum(self.grid[x][y] for (x, y) in cells if self.grid[x][y] != 0)
        return total == target or any(self.grid[x][y] == 0 for (x, y) in cells)

    def check_difference(self, cells, target):
        values = [self.grid[x][y] for (x, y) in cells if self.grid[x][y] != 0]
        return len(values) < 2 or abs(values[0] - values[1]) == target

    def check_product(self, cells, target):
        product = 1
        for (x, y) in cells:
            if self.grid[x][y] == 0:
                return True
            product *= self.grid[x][y]
        return product == target

    def check_division(self, cells, target):
        values = [self.grid[x][y] for (x, y) in cells if self.grid[x][y] != 0]
        return len(values) < 2 or max(values) / min(values) == target

    def solve(self):
        start_time = time.time()
        solved = self.backtrack()
        self.total_solve_time = (time.time() - start_time)*1000
        return solved

    def backtrack(self):
        cell = self.select_unassigned_cell_mrv()
        if cell is None:
            return True
        
        x, y = cell
        for value in list(self.domains[x][y]):
            if self.is_consistent_single(x, y, value):
                self.grid[x][y] = value
                if self.backtrack():
                    return True
                self.grid[x][y] = 0
        return False

    def select_unassigned_cell_mrv(self):
        min_domain_size = float('inf')
        selected_cell = None

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0 and len(self.domains[i][j]) < min_domain_size:
                    min_domain_size = len(self.domains[i][j])
                    selected_cell = (i, j)

        return selected_cell

    def is_consistent_single(self, x, y, value):
        for i in range(self.grid_size):
            if self.grid[x][i] == value or self.grid[i][y] == value:
                return False
        
        for region in self.regions:
            if (x, y) in region.cells:
                if not self.valid_region_value(x, y, value, region.operation, region.target, region.cells):
                    return False
        return True

    def print_grid(self):
        for row in self.grid:
            print("| " + " | ".join(map(str, row)) + " |")

regions = [
    region([(0, 0), (1, 0), (2, 0)], '*', 96),
    region([(0, 1), (0, 2)], '/', 4),
    region([(0, 3), (1, 3), (1, 4)], '*', 18),
    region([(0, 4), (0, 5)], '-', 2),
    region([(0, 6), (0, 7)], '+', 17),
]

csp = CSP(9, regions)
if csp.solve():
    print("Solution found:")
    csp.print_grid()
else:
    print("No solution found.")

print(f"Execution time: {csp.total_solve_time:.2f} ms")
