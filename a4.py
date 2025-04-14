from ortools.sat.python import cp_model
import os

# read the file, remove white spaces, turns it into a 2d list
def read_puzzle(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    grid = []
    for line in lines:
        line = line.strip().replace(" ", "")
        if line:
            grid.append([char for char in line])
    return grid

# helper functions
def letter_to_int(letter):
    # turns a letter into an int by getting the ascii value and using A to have the ints start at 1
    # an underscore will represent 0
    if letter == "_":
        return 0
    return ord(letter) - ord("A") + 1

def int_to_letter(number):
    # same logic as letter to int but reverse
    return "_" if number == 0 else chr(number + ord("A") - 1)

# callback class, collects multiple solutions (limit set to 2)
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, cells, limit=2):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.cells = cells
        self.limit = limit
        self.solutions = []
        self.count = 0

    def OnSolutionCallback(self):
        solution = [[self.Value(self.cells[i][j]) for j in range(25)] for i in range(25)]
        self.solutions.append(solution)
        self.count += 1
        if self.count >= self.limit:
            self.StopSearch()


# main function
def solve_alphadoku(grid):
    # use or tools to create a constraint model
    model = cp_model.CpModel()
    domain = 25
    box_size = 5

    # create variables in the empty grid from 1-25 (a-y)
    cells = [[model.NewIntVar(1, domain, f"cell_{i}_{j}") for j in range(domain)] for i in range(domain)]

    # fill in the cells from the puzzle
    for i in range(domain):
        for j in range(domain):
            if grid[i][j] != "_":
                model.Add(cells[i][j] == letter_to_int(grid[i][j]))

    # ensure that each row contains different values
    for i in range(domain):
        model.AddAllDifferent([cells[i][j] for j in range(domain)])  # row
        model.AddAllDifferent([cells[j][i] for j in range(domain)])  # column

    # ensure that each 5x5 box contains different values
    for box_row in range(0, domain, box_size):
        for box_col in range(0, domain, box_size):
            box_cells = [
                cells[r][c]
                for r in range(box_row, box_row + box_size)
                for c in range(box_col, box_col + box_size)
            ]
            model.AddAllDifferent(box_cells)

    # calling callback class from earlier to look for solutions
    solver = cp_model.CpSolver()
    solution_printer = SolutionCollector(cells, limit=2)
    solver.SearchForAllSolutions(model, solution_printer)

    # prints out first solution it finds, even if it finds another
    if len(solution_printer.solutions) == 0:
        print("no solution.")
    elif len(solution_printer.solutions) == 1:
        print("solution is unique")
    else:
        print("another solution was found, solution isn't unique")

    if solution_printer.solutions:
        print("first solution found:")
        solution = [[int_to_letter(val) for val in row] for row in solution_printer.solutions[0]]
        for i in range(0, 25, 5):
            for row in range(i, i + 5):
                for j in range(0, 25, 5):
                    print(" ".join(solution[row][j:j+5]), end="  ")
                print()
            print()

# path to the puzzles folder
puzzle_folder_path = '/puzzles'

# go through all 30 filse in puzzles folder
for puzzle_file in os.listdir(puzzle_folder_path):
    if puzzle_file.endswith(".txt"):
        print(f"\nsolving {puzzle_file}")
        puzzle_path = os.path.join(puzzle_folder_path, puzzle_file)
        grid = read_puzzle(puzzle_path)
        solve_alphadoku(grid)
