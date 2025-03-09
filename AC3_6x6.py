import time
from collections import deque

class region:
    def __init__(self, cells, operation, target):
        self.cells = cells
        self.operation = operation
        self.target = target

class CSP:
    def __init__(self, grid_size, cages):
        self.grid_size = grid_size
        self.regions = cages
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.domains = [[set(range(1, grid_size + 1)) for _ in range(grid_size)] for _ in range(grid_size)]
        self._initial_constraints()

    def _initial_constraints(self):

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.domains[i][j] = self.filter_domain(i, j, self.domains[i][j])

        for region in self.regions:
            self._region_constraint(region)

    def filter_domain(self, row, col, domain):
        # Remove values already present in the row or column
        for i in range(self.grid_size):
            if self.grid[row][i] in domain:
                domain.remove(self.grid[row][i])
            if self.grid[i][col] in domain:
                domain.remove(self.grid[i][col])
        return domain

    def _region_constraint(self, cage):
        cells = cage.cells
        operation = cage.operation
        target = cage.target

        for (x, y) in cells:
            self.domains[x][y] = self.filter_region_domain(x, y, operation, target, cells)

    def filter_region_domain(self, x, y, operation, target, cells):
        new_domain = set()
        for value in self.domains[x][y]:
            if self.is_valid_region_value(x, y, value, operation, target, cells):
                new_domain.add(value)
        return new_domain

    def is_valid_region_value(self, x, y, value, operation, target, cells):

        original_value = self.grid[x][y]
        self.grid[x][y] = value

        # Check if the cregion constraint is satisfied
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

        # Restore the original value
        self.grid[x][y] = original_value
        return result

    def check_sum(self, cells, target):
        total = 0
        for (x, y) in cells:
            if self.grid[x][y] == 0:
                return True  
            total += self.grid[x][y]
        return total == target

    def check_difference(self, cells, target):
        values = [self.grid[x][y] for (x, y) in cells if self.grid[x][y] != 0]
        if len(values) < 2:
            return True  
        return abs(values[0] - values[1]) == target

    def check_product(self, cells, target):
        product = 1
        for (x, y) in cells:
            if self.grid[x][y] == 0:
                return True  
            product *= self.grid[x][y]
        return product == target

    def check_division(self, cells, target):
        values = [self.grid[x][y] for (x, y) in cells if self.grid[x][y] != 0]
        if len(values) < 2:
            return True  
        return max(values) / min(values) == target

    def ac3(self):
        # Initialize the queue with all arcs (pairs of constrained variables)
        queue = deque()
        for region in self.regions:
            cells = region.cells
            for i in range(len(cells)):
                for j in range(len(cells)):
                    if i != j:
                        queue.append((cells[i], cells[j]))

        # Process the queue
        while queue:
            (xi, yi), (xj, yj) = queue.popleft()
            if self.revise((xi, yi), (xj, yj)):
                if not self.domains[xi][yi]:
                    return False  # No solution
                for region in self.regions:
                    if (xi, yi) in region.cells:
                        for (xk, yk) in region.cells:
                            if (xk, yk) != (xj, yj):
                                queue.append(((xk, yk), (xi, yi)))
        return True

    def revise(self, xi, xj):
        revised = False
        for value in list(self.domains[xi[0]][xi[1]]):
            if not any(self.is_consistent(xi[0], xi[1], value, xj[0], xj[1], y) for y in self.domains[xj[0]][xj[1]]):
                self.domains[xi[0]][xi[1]].remove(value)
                revised = True
        return revised

    def is_consistent(self, xi, yi, value, xj, yj, y):

        original_value = self.grid[xi][yi]
        self.grid[xi][yi] = value

        consistent = True
        for region in self.regions:
            if (xi, yi) in region.cells and (xj, yj) in region.cells:
                if not self.is_valid_region_value(xi, yi, value, region.operation, region.target, region.cells):
                    consistent = False
                    break

        self.grid[xi][yi] = original_value
        return consistent

    def solve(self):
        # Enforce arc-consistency using AC-3 before backtracking
        if not self.ac3():
            return False  
        return self.backtrack()

    def backtrack(self):

        cell = self.select_unassigned_cell()
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

    def select_unassigned_cell(self):

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_consistent_single(self, x, y, value):

        for i in range(self.grid_size):
            if self.grid[x][i] == value or self.grid[i][y] == value:
                return False

        for region in self.regions:
            if (x, y) in region.cells:
                if not self.is_valid_region_value(x, y, value, region.operation, region.target, region.cells):
                    return False
        return True

    def print_grid(self):
        for row in self.grid:
            print("| " + " | ".join(map(str, row)) + " |")

# Example usage
grid_size = 6
regions = [
    region([(0, 0), (1, 0)], '-', 4),
    region([(0, 1), (1, 1)], '-', 1),
    region([(0, 2), (0, 3)], '-', 3),
    region([(0, 4), (0, 5)], '/', 3),
    region([(1, 2), (1, 3)], '-', 1),
    region([(1, 4), (1, 5), (2, 4)], '*', 150),
    region([(2, 0), (2, 1), (3, 0)], '+', 7),
    region([(2, 2), (2, 3)], '-', 2),
    region([(2, 5), (3, 5)], '+', 5),
    region([(3, 1), (3, 2)], '-', 1),
    region([(3, 3), (3, 4)], '/', 3),
    region([(4, 0)], ' ', 3),
    region([(4, 1), (4, 2), (5, 2)], '*', 60),
    region([(4, 3), (5, 3)], '-', 4),
    region([(4, 4), (5, 4)], '-', 1),
    region([(4, 5), (5, 5)], '-', 3),
    region([(5, 0), (5, 1)], '/', 3),
]

# Start the timer
start_time = time.time()

# Solve the puzzle
csp = CSP(grid_size, regions)
if csp.solve():
    print("Solution found:")
    csp.print_grid()
else:
    print("No solution found.")

# Calculate and print the execution time in ms 
end_time = time.time()
execution_time = (end_time - start_time) * 1000
print(f"Execution time: {execution_time:.2f} ms")