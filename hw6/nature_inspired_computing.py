import numpy as np
import pandas as pd
from evo import Environment
import random
import csv

sections_df = pd.read_csv('sections.csv')
tas_df = pd.read_csv('tas.csv')

def create_random_solution(num_tas, num_sections):
    solution = np.random.choice([0, 1], size=(num_tas, num_sections))
    return solution

def overallocation(solution):
    overallocation_penalty = 0
    for ta_idx, ta_row in enumerate(solution):
        max_assigned = tas_df.loc[ta_idx, 'max_assigned']
        assigned_count = np.sum(ta_row)
        if assigned_count > max_assigned:
            overallocation_penalty += assigned_count - max_assigned
    return overallocation_penalty

def conflicts(solution):
    conflict_count = 0
    for ta_idx, ta_row in enumerate(solution):
        assigned_sections = np.where(ta_row == 1)[0]
        daytimes = sections_df.loc[assigned_sections, 'daytime'].tolist()
        if len(set(daytimes)) < len(daytimes):
            conflict_count += 1
    return conflict_count

def undersupport(solution):
    undersupport_penalty = 0
    for section_idx, section_row in enumerate(solution.T):
        min_ta = sections_df.loc[section_idx, 'min_ta']
        assigned_count = np.sum(section_row)
        if assigned_count < min_ta:
            undersupport_penalty += min_ta - assigned_count
    return undersupport_penalty

def unwilling(solution):
    unwilling_count = 0
    for ta_idx, ta_row in enumerate(solution):
        assigned_sections = np.where(ta_row == 1)[0]
        for section_idx in assigned_sections:
            if tas_df.iloc[ta_idx, section_idx+3] == 'U':
                unwilling_count += 1
    return unwilling_count

def unpreferred(solution):
    unpreferred_count = 0
    for ta_idx, ta_row in enumerate(solution):
        assigned_sections = np.where(ta_row == 1)[0]
        for section_idx in assigned_sections:
            if tas_df.iloc[ta_idx, section_idx+3] == 'W':
                unpreferred_count += 1
    return unpreferred_count

def agent1(solutions):
    solution = random.choice(solutions)
    ta_idx = random.randint(0, solution.shape[0] - 1)
    section_idx = random.randint(0, solution.shape[1] - 1)
    solution[ta_idx, section_idx] = 1 - solution[ta_idx, section_idx]
    return solution

def agent2(solutions):
    solution1 = random.choice(solutions)
    solution2 = random.choice(solutions)
    crossover_point = random.randint(1, solution1.shape[0] - 1)
    new_solution = np.vstack((solution1[:crossover_point], solution2[crossover_point:]))
    return new_solution

def agent3(solutions):
    solution = random.choice(solutions)
    ta_idx = random.randint(0, solution.shape[0] - 1)
    assigned_sections = np.where(solution[ta_idx] == 1)[0]
    if len(assigned_sections) > 0:
        section_idx = random.choice(assigned_sections)
        solution[ta_idx, section_idx] = 0
    return solution

def agent4(solutions):
    solution = random.choice(solutions)
    section_idx = random.randint(0, solution.shape[1] - 1)
    min_ta = sections_df.loc[section_idx, 'min_ta']
    assigned_tas = np.where(solution[:, section_idx] == 1)[0]
    if len(assigned_tas) < min_ta:
        available_tas = [ta_idx for ta_idx in range(solution.shape[0]) if solution[ta_idx, section_idx] == 0]
        if len(available_tas) > 0:
            ta_idx = random.choice(available_tas)
            solution[ta_idx, section_idx] = 1
    return solution

env = Environment()
env.add_fitness_criteria('overallocation', overallocation)
env.add_fitness_criteria('conflicts', conflicts)
env.add_fitness_criteria('undersupport', undersupport)
env.add_fitness_criteria('unwilling', unwilling)
env.add_fitness_criteria('unpreferred', unpreferred)

env.add_agent('agent1', agent1)
env.add_agent('agent2', agent2)
env.add_agent('agent3', agent3)
env.add_agent('agent4', agent4)

num_tas = len(tas_df)
num_sections = len(sections_df)
for _ in range(100):
    solution = create_random_solution(num_tas, num_sections)
    env.add_solution(solution)

env.evolve(n=1000000, dom=100, status=1000, time_limit=600)

best_solutions = env.pop

summary_data = []
for eval, solution in best_solutions.items():
    summary_data.append(['DanVivRu', eval[0][1], eval[1][1], eval[2][1], eval[3][1], eval[4][1]])

# Write the summary table to a CSV file
with open('summary.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['groupname', 'overallocation', 'conflicts', 'undersupport', 'unwilling', 'unpreferred'])
    writer.writerows(summary_data)

test1_solution = np.genfromtxt('test1.csv', delimiter=',')
test2_solution = np.genfromtxt('test2.csv', delimiter=',')
test3_solution = np.genfromtxt('test3.csv', delimiter=',')

test_solutions = [test1_solution, test2_solution, test3_solution]
test_scores = []
for solution in test_solutions:
    scores = [
        overallocation(solution),
        conflicts(solution),
        undersupport(solution),
        unwilling(solution),
        unpreferred(solution)
    ]
    test_scores.append(scores)

print("Test Solution Scores:")
print("Objective\tTest1\tTest2\tTest3")
objectives = ['Overallocation', 'Conflicts', 'Undersupport', 'Unwilling', 'Unpreferred']
for obj, scores in zip(objectives, zip(*test_scores)):
    print(f"{obj}\t{scores[0]}\t{scores[1]}\t{scores[2]}")

print("\nBest Solutions:")
print("Group\tOverallocation\tConflicts\tUndersupport\tUnwilling\tUnpreferred")
for eval, solution in best_solutions.items():
    print(f"DanVivRu\t{eval[0][1]}\t{eval[1][1]}\t{eval[2][1]}\t{eval[3][1]}\t{eval[4][1]}")

# Choose the best solution based on your preference
best_solution = list(best_solutions.values())[0]

print("\nBest Solution Details:")
print("TA Assignments:")
for ta_idx, ta_row in enumerate(best_solution):
    assigned_sections = np.where(ta_row == 1)[0]
    print(f"TA {ta_idx}: {list(assigned_sections)}")

print("\nSection Assignments:")
for section_idx, section_row in enumerate(best_solution.T):
    assigned_tas = np.where(section_row == 1)[0]
    print(f"Section {section_idx}: {list(assigned_tas)}")

print("\nBest Solution Scores:")
best_scores = [
    overallocation(best_solution),
    conflicts(best_solution),
    undersupport(best_solution),
    unwilling(best_solution),
    unpreferred(best_solution)
]
for obj, score in zip(objectives, best_scores):
    print(f"{obj}: {score}")