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
    print("Initial Formula:", formula)
    print("Initial Assignment:", assignment)
    
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
        clauses, assignment = unit_propagate(clauses, assignment)
        if not clauses:
            return assignment  
        if any(not c for c in clauses):
            return None  

        var = abs(clauses[0][0])
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_clauses = [c for c in clauses if (var if val else -var) not in c]
            new_clauses = [list(filter(lambda x: x != (-var if val else var), c)) for c in new_clauses]
            result = dpll_recursive(new_clauses, new_assignment)
            if result is not None:
                return result

        return None  

    assignment = dpll_recursive(formula, assignment)

    print("DPLL finished. Final Assignment:", assignment)
    end_time = time.time()
    print("DPLL took", end_time - start_time, "seconds")
    
    return assignment, end_time - start_time, sum(assignment.values()) if assignment else None


# walksat
def walksat(formula, max_flips=10000, p=0.5):
    assignment = {i + 1: False for i in range(len(formula))}
    start_time = time.time()

    for flip_count in range(max_flips):
        unsatisfied_clauses = [clause for clause in formula if not any(assignment[abs(lit)] == (lit > 0) for lit in clause)]

        if not unsatisfied_clauses:
            print("All clauses satisfied!")
            break
        
        clause = random.choice(unsatisfied_clauses)
        flip_var = max(clause, key=lambda lit: sum(assignment[abs(lit)] == (lit > 0) for lit in clause))
        assignment[abs(flip_var)] = not assignment[abs(flip_var)]  # Use abs() to update the assignment

    end_time = time.time()
    print("WalkSAT finished. Final Assignment:", assignment)
    print("WalkSAT took", end_time - start_time, "seconds")
    
    return assignment, end_time - start_time, sum(assignment.values()) if assignment else None


# genetic algorithm
def genetic_algorithm(formula, population_size=50, generations=100, mutation_rate=0.1):

    print("Starting Genetic Algorithm...")
    start_time = time.time()

    num_vars = len(set(abs(lit) for clause in formula for lit in clause))

    def fitness(assignment):
        return sum(
            any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)  
            for clause in formula
        )

    population = [np.random.choice([True, False], num_vars) for _ in range(population_size)]

    for generation in range(generations):
        scores = [fitness(ind) for ind in population]
        if max(scores) == len(formula):
            best_ind = population[scores.index(max(scores))]
            end_time = time.time()
            return {i + 1: bool(val) for i, val in enumerate(best_ind)}, end_time - start_time, sum(best_ind)

        new_population = []
        for _ in range(population_size // 2):
            parents = random.choices(population, weights=scores, k=2)
            crossover_point = random.randint(0, num_vars - 1)
            child1 = np.concatenate((parents[0][:crossover_point], parents[1][crossover_point:]))
            child2 = np.concatenate((parents[1][:crossover_point], parents[0][crossover_point:]))
            new_population.extend([child1, child2])

        for individual in new_population:
            if random.random() < mutation_rate:
                individual[random.randint(0, num_vars - 1)] = not individual[random.randint(0, num_vars - 1)]

        population = new_population

    end_time = time.time()
    return None, end_time - start_time, None  


# run experiments and save to txt file
def save_results_to_file(results, filename="results.txt"):
    with open(filename, "w") as f:
        for result in results:
            f.write(f"Formula {result['Formula']} - Algorithm: {result['Algorithm']}\n")
            f.write(f"Time Taken: {result['Time']:.6f} seconds\n")
            f.write(f"Best c value: {result['Best c']}\n\n")

def run_experiments(file_path):
    formulas = load_formulas(file_path)
    results = []
    
    for i, formula in enumerate(formulas):
        print(f"Running algorithm on Formula {i + 1}...")
        for algo_name, algo in [("DPLL", dpll), ("WalkSAT", walksat), ("Genetic", genetic_algorithm)]:
            start_time = time.time()
            solution, time_taken, c_value = algo(formula)
            print(f"{algo_name} finished for Formula {i + 1}. Time taken: {time_taken} seconds.")
            results.append({
                "Formula": i + 1,
                "Algorithm": algo_name,
                "Time": time_taken,
                "Best c": c_value
            })
    
    save_results_to_file(results)
    return results

results = run_experiments("A3Formulas")
