import sys
import random
import itertools
from itertools import product

# hard code the given probabilities from the cpt tables
P_B = {True: 0.02, False: 0.98}
P_E = {True: 0.03, False: 0.97}
P_A_given_BE = {
    (True, True): {True: 0.97, False: 0.03},
    (True, False): {True: 0.92, False: 0.08},
    (False, True): {True: 0.36, False: 0.64},
    (False, False): {True: 0.03, False: 0.97}
}
P_J_given_A = {True: {True: 0.85, False: 0.15},
               False: {True: 0.07, False: 0.93}}
P_M_given_A = {True: {True: 0.69, False: 0.31},
               False: {True: 0.02, False: 0.98}}

# variable order from top down
VARIABLES = ['B', 'E', 'A', 'J', 'M']

# calculate joint probability
def get_probability_full_joint(assignment):
    # chain rule
    b, e, a, j, m = assignment['B'], assignment['E'], assignment['A'], assignment['J'], assignment['M']
    prob = (
        P_B[b] *
        P_E[e] *
        P_A_given_BE[(b, e)][a] *
        P_J_given_A[a][j] *
        P_M_given_A[a][m]
    )
    return prob

# inference by enumeration
def enumerate_all(variables, evidence):
    if not variables:
        return 1.0
    first = variables[0]
    rest = variables[1:]
    if first in evidence:
        return get_probability_full_joint(evidence) * enumerate_all(rest, evidence)
    else:
        total = 0
        for value in [True, False]:
            extended = evidence.copy()
            extended[first] = value
            total += get_probability_full_joint(extended)
        return total

def exact_inference(c1, c2):
    # merge the two conditions
    known = c1.copy()
    known.update(c2)

    # helper function to generate all combinations of hidden vars
    def extend(known, hidden_vars):
        all_assignments = []
        for values in itertools.product([True, False], repeat=len(hidden_vars)):
            assignment = known.copy()
            for var, val in zip(hidden_vars, values):
                assignment[var] = val
            all_assignments.append(assignment)
        return all_assignments

    # find hidden vars (not in c1 or c2)
    hidden_vars = [var for var in ['B', 'E', 'A', 'J', 'M'] if var not in known]
    
    # numerator: P(c1 and c2)
    numerator = sum(get_probability_full_joint(a) for a in extend(known, hidden_vars))
    
    # denominator; need to find hidden vars missing from c2 only
    hidden_vars_for_denominator = [var for var in ['B', 'E', 'A', 'J', 'M'] if var not in c2]
    
    denominator = sum(get_probability_full_joint(a) for a in extend(c2, hidden_vars_for_denominator))
    
    print("numerator: {}, denominator: {}".format(numerator, denominator))  # debugging line
    return numerator / denominator

# rejection sampling
def rejection_sampling(c1, c2, N=1000000):
    def prior_sample():
        b = random.random() < P_B[True]
        e = random.random() < P_E[True]
        a = random.random() < P_A_given_BE[(b, e)][True]
        j = random.random() < P_J_given_A[a][True]
        m = random.random() < P_M_given_A[a][True]
        return {'B': b, 'E': e, 'A': a, 'J': j, 'M': m}

    def matches(evidence, sample):
        return all(sample[k] == v for k, v in evidence.items())

    count_accepted = 0
    count_matching = 0
    for _ in range(N):
        sample = prior_sample()
        if matches(c2, sample):
            count_accepted += 1
            if matches(c1, sample):
                count_matching += 1

    print("samples accepted: {}, matching: {}".format(count_accepted, count_matching))  # debugging line
    if count_accepted == 0:
        print("no samples accepted")
        return 0
    return count_matching / count_accepted

# parses arguments given in command line
def parse_args(args):
    if 'given' in args:
        idx = args.index('given')
        c1_args = args[:idx]
        c2_args = args[idx + 1:]
    else:
        c1_args = args
        c2_args = []

    def parse_event(arg):
        var = arg[0]
        val = arg[1] == 't'
        return (var.upper(), val)

    c1 = dict(parse_event(a) for a in c1_args)
    c2 = dict(parse_event(a) for a in c2_args)

    return c1, c2

# main function
def main():
    args = sys.argv[1:]
    if not (1 <= len(args) <= 6):
        print("commands: a5.py <events> [given <conditions>]")
        return

    c1, c2 = parse_args(args)
    exact = exact_inference(c1, c2)
    approx = rejection_sampling(c1, c2)

    print("\ninference by enumeration: {:.5f}".format(exact))
    print("rejection sampling with {} samples: {:.5f}".format(1000000, approx))

if __name__ == '__main__':
    main()
