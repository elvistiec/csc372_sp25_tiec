import time
import random
import numpy as np

# load all 32 formulas
def load_formulas(file_path):
    formulas = []

    return formulas

# dpll
def dpll(formula, assignment={}):
    start_time = time.time()

    end_time = time.time()
    return assignment, end_time - start_time, None 

# walksat
def walksat(formula, max_flips=10000, p=0.5):
    start_time = time.time()

    end_time = time.time()
    return None, end_time - start_time, None  

# genetic algorithm
def genetic_algorithm(formula, population_size=50, generations=100, mutation_rate=0.1):
    start_time = time.time()

    end_time = time.time()
    return None, end_time - start_time, None  

# function that runs the experiments
def run_experiments(file_path):
    formulas = load_formulas(file_path)
    results = []
    
    for i, formula in enumerate(formulas):
        for algo_name, algo in [("DPLL", dpll), ("WalkSAT", walksat), ("Genetic", genetic_algorithm)]:
            runs = 10 if algo_name in ["WalkSAT", "Genetic"] else 1
            
            for run in range(runs):
                solution, time_taken, c_value = algo(formula)
                results.append({
                    "Formula": i + 1,
                    "Algorithm": algo_name,
                    "Run": run + 1,
                    "Time": time_taken,
                    "Best c": c_value
                })
    
    return results

