import time  

class region:
    def __init__(self, cells, operation, target):
        self.cells = cells
        self.operation = operation
        self.target = target

class MRV_6x6:
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

        for region in self.regions:
            self._region_constraint(region)

    def filter_domain(self, row, col, domain):

        for i in range(self.grid_size):
            if self.grid[row][i] in domain:
                domain.remove(self.grid[row][i])
            if self.grid[i][col] in domain:
                domain.remove(self.grid[i][col])
        return domain

    def _region_constraint(self, region):
        cells = region.cells
        operation = region.operation
        target = region.target

        for (x, y) in cells:
            self.domains[x][y] = self.filter_region_domain(x, y, operation, target, cells)

    def filter_region_domain(self, x, y, operation, target, cells):
        new_domain = set()
        for value in self.domains[x][y]:
            if self.valid_region_value(x, y, value, operation, target, cells):
                new_domain.add(value)
        return new_domain

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

    def solve(self):
        return self.backtrack()

    def backtrack(self):
        # Find the next cell to assign using MRV
        cell = self.select_unassigned_cell()
        if cell is None:
            return True  

        x, y = cell
        for value in list(self.domains[x][y]):  
            if self.is_consistent(x, y, value):
                self.grid[x][y] = value
                if self.backtrack():
                    return True
                self.grid[x][y] = 0  
        return False

    def select_unassigned_cell(self):
        # MRV heuristic: select the cell with the smallest domain
        min_domain_size = float('inf')
        selected_cell = None
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0 and len(self.domains[i][j]) < min_domain_size:
                    min_domain_size = len(self.domains[i][j])
                    selected_cell = (i, j)
        return selected_cell

    def is_consistent(self, x, y, value):
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

start_time = time.time()

csp = MRV_6x6(grid_size, regions)
if csp.solve():
    print("Solution found:")
    csp.print_grid()
else:
    print("No solution found.")

end_time = time.time()
execution_time = (end_time - start_time)*1000
print(f"Execution time: {execution_time:.2f} ms")