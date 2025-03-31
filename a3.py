import time
import random
import numpy as np
import os

# load all 32 formulas
def load_formulas(folder_path):
    formulas = []
    
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".cnf"): 
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as f:
                clauses = []
                for line in f:
                    line = line.strip()
                    if line.startswith("c") or line.startswith("p"):  
                        continue  # skip the seed and cnf line
                    clause = list(map(int, line.split()))[:-1]  # remove the 0 at the end of the cnf form
                    if clause:
                        clauses.append(clause)
                formulas.append(clauses)

    return formulas

# dpll
def dpll(formula, assignment={}):
    node_count = 0 # keep track of nodes
    start_time = time.time()

    if all(literal in assignment for clause in formula for literal in clause):
        print("All variables assigned, checking satisfaction...")

    def unit_propagate(clauses, assignment):
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            for unit in unit_clauses:
                lit = unit[0]
                assignment[abs(lit)] = lit > 0
                clauses = [c for c in clauses if lit not in c]
                clauses = [list(filter(lambda x: x != -lit, c)) for c in clauses]
        return clauses, assignment

    def dpll_recursive(clauses, assignment):
        nonlocal node_count
        node_count += 1
        clauses, assignment = unit_propagate(clauses, assignment)

        if not clauses:
            return assignment  
        if any(not c for c in clauses):
            return None  

        var = abs(clauses[0][0])  # pick a variable to try
        for val in [True, False]:  # try both true and false for the variable
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_clauses = [c for c in clauses if (var if val else -var) not in c]
            new_clauses = [list(filter(lambda x: x != (-var if val else var), c)) for c in new_clauses]
            result = dpll_recursive(new_clauses, new_assignment)
            if result is not None:
                return result

        return None  

    assignment = dpll_recursive(formula, assignment)

    # if we have a solution, it is satisfiable; otherwise, unsatisfiable
    end_time = time.time()
    print(f"DPLL finished. Time: {end_time - start_time:.4f} seconds, Nodes expanded: {node_count}")
    
    return assignment, end_time - start_time, node_count

# walksat
def walksat(formula, max_flips=10000, p=0.5):
    assignment = {i + 1: False for i in range(len(formula))}
    start_time = time.time()

    # initialize a variable to track the largest number of satisfied clauses
    flips = 0
    max_satisfied_clauses = 0

    for flip_count in range(max_flips):
        unsatisfied_clauses = [clause for clause in formula if not any(assignment[abs(lit)] == (lit > 0) for lit in clause)]

        if not unsatisfied_clauses:  # All clauses satisfied
            end_time = time.time()
            # output time and flips for satisfiable problems
            print(f"WalkSAT finished in {end_time - start_time:.4f} seconds with {flip_count} flips.")
            return assignment, end_time - start_time, len(formula)  # all clauses are satisfied

        # track the number of satisfied clauses
        satisfied_clauses_count = len(formula) - len(unsatisfied_clauses)
        max_satisfied_clauses = max(max_satisfied_clauses, satisfied_clauses_count)

        # perform the WalkSAT flip step
        clause = random.choice(unsatisfied_clauses)
        flip_var = max(clause, key=lambda lit: sum(assignment[abs(lit)] == (lit > 0) for lit in clause))
        assignment[abs(flip_var)] = not assignment[abs(flip_var)]  # use abs() to update the assignment

    end_time = time.time()

    # report the largest number of clauses satisfied for unsatisfiable problems
    print(f"WalkSAT finished after {max_flips} flips.")
    print(f"Largest number of clauses satisfied: {max_satisfied_clauses}")
    return None, end_time - start_time, max_satisfied_clauses

# genetic
def genetic_algorithm(formula, population_size=50, generations=100, mutation_rate=0.1):
    start_time = time.time()

    num_vars = len(set(abs(lit) for clause in formula for lit in clause))

    # fitness function with penalties for unsatisfied clauses
    def fitness(assignment):
        satisfied = sum(
            any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)
            for clause in formula
        )
        return satisfied  # only return the number of satisfied clauses

    # initialize population with random truth assignments
    population = [np.random.choice([True, False], num_vars) for _ in range(population_size)]

    best_solution = None
    best_fitness = -1

    for generation in range(generations):
        scores = [fitness(ind) for ind in population]
        max_fitness = max(scores)

        # if we find a solution that satisfies all clauses, we return it
        if max_fitness == len(formula):
            best_ind = population[scores.index(max_fitness)]
            end_time = time.time()
            return {i + 1: bool(val) for i, val in enumerate(best_ind)}, end_time - start_time, len(formula)

        # track the best solution found so far
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_solution = population[scores.index(best_fitness)]

        # create the next generation using selection, crossover, and mutation
        new_population = []
        for _ in range(population_size // 2):
            parents = random.choices(population, weights=scores, k=2)
            crossover_point = random.randint(0, num_vars - 1)

            # crossover
            child1 = np.concatenate((parents[0][:crossover_point], parents[1][crossover_point:]))
            child2 = np.concatenate((parents[1][:crossover_point], parents[0][crossover_point:]))

            new_population.extend([child1, child2])

        # mutation
        for individual in new_population:
            if random.random() < mutation_rate:
                individual[random.randint(0, num_vars - 1)] = not individual[random.randint(0, num_vars - 1)]

        population = new_population

    # if no perfect solution was found, return the best solution found
    end_time = time.time()
    if best_solution is not None:
        # check if best fitness equals the total number of clauses
        if best_fitness == len(formula):
            return {i + 1: bool(val) for i, val in enumerate(best_solution)}, end_time - start_time, best_fitness
        else:
            # if the best fitness is not equal to the number of clauses, it's unsatisfiable
            return None, end_time - start_time, best_fitness

    return None, end_time - start_time, best_fitness


def run_experiments(file_path, output_file="results.txt"):
    formulas = load_formulas(file_path)
    results = []
    
    with open(output_file, "w") as f:
        for i, formula in enumerate(formulas):
            f.write(f"Formula {i + 1}\n")
            
            # dpll 1 run
            solution, time_taken, node_count = dpll(formula)
            f.write(f"DPLL: Time={time_taken:.4f} seconds, Nodes expanded={node_count}\n")
            
            # walksat 10 runs
            for j in range(10):
                solution, time_taken, result = walksat(formula)
                if solution is not None:  # satisfiable
                    f.write(f"WalkSAT Run {j+1}: Time={time_taken:.4f} seconds, Flips={result}\n")
                else:  # unsatisfiable
                    f.write(f"WalkSAT Run {j+1}: Time={time_taken:.4f} seconds, Max satisfied={result}\n")
            
            # genetic 10 runs
            for j in range(10):
                solution, time_taken, result = genetic_algorithm(formula)
                if solution is not None:  # satisfiable
                    f.write(f"Genetic Run {j+1}: Time={time_taken:.4f} seconds, Flips={result}\n")
                else:  # unsatisfiable
                    f.write(f"Genetic Run {j+1}: Time={time_taken:.4f} seconds, Max satisfied={result}\n")
            
            f.write("\n")
    
    print(f"Results saved to {output_file}")

run_experiments("A3Formulas")
