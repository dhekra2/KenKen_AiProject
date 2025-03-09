import time

class forwardchecking_4x4:
    N = 4
    
    def __init__(self):
        self.grid = [[0] * self.N for _ in range(self.N)]
        self.domains = [[set(range(1, self.N + 1)) for _ in range(self.N)] for _ in range(self.N)]
        self.forward_checking_time = 0  # Variable to store forward checking time
        self.regions = self.initialize_regions()

    def initialize_regions(self):
        return [
            {'cells': [(0, 0), (0, 1), (1, 0)], 'operation': '*', 'target': 24},
            {'cells': [(0, 2), (0, 3)], 'operation': '/', 'target': 2},
            {'cells': [(1, 1), (1, 2)], 'operation': '-', 'target': 3},
            {'cells': [(1, 3), (2, 3)], 'operation': '-', 'target': 1},
            {'cells': [(2, 0), (2, 1)], 'operation': '+', 'target': 5},
            {'cells': [(2, 2), (3, 2), (3, 3)], 'operation': '+', 'target': 6},
            {'cells': [(3, 0), (3, 1)], 'operation': '-', 'target': 3},
        ]
    
    def solve(self):
        start_time = time.time()
        result = self.backtrack_with_forward_checking()
        solve_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        return result, solve_time

    def backtrack_with_forward_checking(self):
        if self.is_grid_complete():
            return self.validate_regions()
        
        row, col = self.find_unassigned_cell()
        if row is None:
            return False
        
        for value in sorted(self.domains[row][col]):
            if self.is_valid_assignment(row, col, value):
                self.grid[row][col] = value
                domain_backup = self.create_domain_backup()
                
                # Measure forward checking time
                forward_start = time.time()
                if self.forward_check(row, col):
                    forward_checking_duration = (time.time() - forward_start) * 1000  # Convert to milliseconds
                    self.forward_checking_time += forward_checking_duration
                    if self.backtrack_with_forward_checking():
                        return True
                
                self.grid[row][col] = 0
                self.restore_domains(domain_backup)
        
        return False

    def find_unassigned_cell(self):
        for row in range(self.N):
            for col in range(self.N):
                if self.grid[row][col] == 0:
                    return row, col
        return None, None

    def forward_check(self, row, col):
        value = self.grid[row][col]
        for i in range(self.N):
            if i != col and self.grid[row][i] == 0:
                self.domains[row][i].discard(value)
                if not self.domains[row][i]:
                    return False
            if i != row and self.grid[i][col] == 0:
                self.domains[i][col].discard(value)
                if not self.domains[i][col]:
                    return False
        return self.validate_region_constraints_after_assignment(row, col)

    def validate_region_constraints_after_assignment(self, row, col):
        for cage in self.regions:
            if (row, col) in cage['cells']:
                if not self.can_satisfy_region_constraint(cage):
                    return False
        return True

    def can_satisfy_region_constraint(self, cage):
        assigned_values = [self.grid[r][c] for r, c in cage['cells'] if self.grid[r][c] != 0]
        unassigned_cells = [cell for cell in cage['cells'] if self.grid[cell[0]][cell[1]] == 0]
        
        if not unassigned_cells:
            return self.check_region_constraint(assigned_values, cage['operation'], cage['target'])
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
    
    def is_valid_assignment(self, row, col, value):
        return all(self.grid[row][i] != value for i in range(self.N)) and \
               all(self.grid[i][col] != value for i in range(self.N))
    
    def validate_regions(self):
        for region in self.regions:
            values = [self.grid[r][c] for r, c in region['cells']]
            if not self.check_region_constraint(values, region['operation'], region['target']):
                return False
        return True
    
    def create_domain_backup(self):
        return [[set(col) for col in row] for row in self.domains]
    
    def restore_domains(self, backup):
        self.domains = [[set(col) for col in row] for row in backup]
    
    def is_grid_complete(self):
        return all(all(cell != 0 for cell in row) for row in self.grid)
    
    def print_grid(self):
        for row in self.grid:
            print(row)
    
    def print_performance_metrics(self):
        print(f"Forward Checking Time: {self.forward_checking_time:.6f} ms")

if __name__ == "__main__":
    solver = forwardchecking_4x4()
    result, solve_time = solver.solve()
    if result:
        solver.print_grid()
        solver.print_performance_metrics()
    else:
        print("No solution found.")
