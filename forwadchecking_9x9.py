import time

class region:
    def __init__(self, cells, operation, target):
        self.cells = cells
        self.operation = operation
        self.target = target

def kenken_solver(grid_size, regions):
    def is_valid_assignment(solution):

        for i in range(grid_size):
            row_values = solution[i]
            col_values = [solution[j][i] for j in range(grid_size)]
            if len(set(row_values)) != grid_size or len(set(col_values)) != grid_size:
                return False
        
        for region in regions:
            region_values = [solution[r][c] for r, c in region.cells]
            
            if region.operation == '+':
                if sum(region_values) != region.target:
                    return False
            elif region.operation == '*':
                prod = 1
                for val in region_values:
                    prod *= val
                if prod != region.target:
                    return False
            elif region.operation == '-':
                if abs(region_values[0] - region_values[1]) != region.target:
                    return False
            elif region.operation == '/':
                if max(region_values) / min(region_values) != region.target:
                    return False
            elif region.operation == ' ':  # Single cell
                if region_values[0] != region.target:
                    return False
        
        return True

    def forward_check(solution, row, col):
        remaining_values = set(range(1, grid_size + 1))
        
        # Remove values already in the row and column
        remaining_values -= set(solution[row])
        remaining_values -= set(solution[r][col] for r in range(grid_size))
        
        for region in regions:
            if (row, col) in region.cells:
                region_cells = [c for c in region.cells if c != (row, col)]
                for r, c in region_cells:
                    if solution[r][c] != 0:
                        remaining_values = {
                            val for val in remaining_values 
                            if is_valid_partial_region(solution, region, val, (row, col))
                        }
        
        return list(remaining_values)

    def is_valid_partial_region(solution, region, new_val, new_cell):
        region_values = [solution[r][c] for r, c in region.cells if solution[r][c] != 0]
        region_values.append(new_val)
        
        if len(region_values) != len(region.cells):
            return True
        
        if region.operation == '+':
            return sum(region_values) == region.target
        elif region.operation == '*':
            prod = 1
            for val in region_values:
                prod *= val
            return prod == region.target
        elif region.operation == '-':
            return abs(region_values[0] - region_values[1]) == region.target
        elif region.operation == '/':
            return max(region_values) / min(region_values) == region.target
        elif region.operation == ' ':
            return region_values[0] == region.target
        
        return True

    def backtrack(solution, row, col):
        if row == grid_size:
            return solution if is_valid_assignment(solution) else None
        
        next_row, next_col = (row, col + 1) if col < grid_size - 1 else (row + 1, 0)
        
        possible_values = forward_check(solution, row, col)
        
        for val in possible_values:
            solution[row][col] = val
            
            result = backtrack(solution, next_row, next_col)
            if result:
                return result
            
            solution[row][col] = 0
        
        return None

    initial_solution = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    return backtrack(initial_solution, 0, 0)

grid_size = 9
regions = [
    region([(0, 0), (1, 0), (2, 0)], '*', 96),
    region([(0, 1), (0, 2)], '/', 4),
    region([(0, 3), (1, 3), (1, 4)], '*', 18),
    region([(0, 4), (0, 5)], '-', 2),
    region([(0, 6), (0, 7)], '+', 17),
    region([(0, 8), (1, 7), (1, 8)], '*', 294),
    region([(1, 1), (1, 2)], '*', 20),
    region([(1, 5), (1, 6), (2, 5), (2, 6)], '*', 168),
    region([(2, 1), (2, 2)], '-', 5),
    region([(2, 3), (3, 3)], '/', 3),
    region([(2, 4), (3, 4), (3, 5), (3, 6)], '*', 70),
    region([(2, 7), (2, 8)], '-', 1),
    region([(3, 0), (4, 0)], '-', 2),
    region([(3, 1), (4, 1)], '-', 3),
    region([(3, 2), (4, 2)], '/', 4),
    region([(3, 7), (3, 8), (4, 8)], '*', 32),
    region([(4, 3), (5, 3)], '/', 2),
    region([(4, 4), (4, 5), (5, 5)], '*', 18),
    region([(4, 6), (4, 7)], '-', 1),
    region([(5, 0), (5, 1), (6, 1), (6, 2)], '*', 50),
    region([(5, 2)], ' ', 7),
    region([(5, 4), (6, 4)], '/', 2),
    region([(5, 6), (5, 7), (6, 7)], '+', 15),
    region([(5, 8), (6, 8), (7, 8)], '+', 14),
    region([(6, 0), (7, 0)], '/', 4),
    region([(6, 3)], ' ', 6),
    region([(6, 5), (6, 6)], '-', 2),
    region([(7, 1), (7, 2), (7, 3)], '+', 19),
    region([(7, 4), (8, 4)], '-', 2),
    region([(7, 5), (8, 5)], '-', 1),
    region([(7, 6), (7, 7)], '+', 6),
    region([(8, 0), (8, 1)], '-', 4),
    region([(8, 2), (8, 3)], '-', 1),
    region([(8, 6), (8, 7)], '/', 2),
    region([(8, 8)], ' ', 4),
]

start_time = time.time()
solution = kenken_solver(grid_size, regions)

if solution:
    print("Solution found:")
    for row in solution:
        print("| " + " | ".join(map(str, row)) + " |")
else:
    print("No solution found.")

end_time = time.time()
print(f"Execution time: {(end_time - start_time) * 1000:2f} ms")
