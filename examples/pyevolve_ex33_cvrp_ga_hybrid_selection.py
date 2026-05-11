import argparse
import collections
import os
import time
from itertools import combinations

import numpy as np
import skfuzzy as fuzz
import tsplib95
from scipy.stats import entropy
from skfuzzy import control as ctrl

from pyevolve import Consts
from pyevolve import GSimpleGA
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.perturbations.CrossoverG1DListPermutations import *
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.representations import G1DList
from pyevolve.selections.SelectionRank import *
from pyevolve.selections.Selectors import GTournamentSelector

collections.Callable = collections.abc.Callable

from helper_tsp import dict_crossoever_operators, crossover_methods



dict_selector_operators = {
    "FPS": SelectorFitnessProportional,
    "LRS": SelectorLinearRanking,
    "ERS": SelectorExponentialRanking,
    "EEBS": SelectorExplorationExploitationBalance,
    "SRS": SelectorSplitRanking,
    "NTS": SelectorNewTournament,
    "TS": GTournamentSelector,
}

DIST_MATRIX = {}
DEMANDS = {}
CAPACITY = 0
CITIES_COUNT = 0
DEPOT_INDEX = 0
LAST_SCORE = -1
GENERATION_COUNT = 1001

strategy = "deterministic"
#strategy="fuzzy"
#strategy="entropy"
#strategy="adaptive"
#strategy="selfadaptive"
#strategy="qlearning"
#strategy="bandit"


Q_table = np.zeros((5, 5, 5))
prev_state = (0, 0)
prev_action = 2
alpha_bins = [0.1, 0.3, 0.5, 0.7, 0.9]
rewards = [0.0] * len(alpha_bins)
counts = [0] * len(alpha_bins)


diversity = ctrl.Antecedent(np.linspace(0, 1, 101), 'diversity')
iteration = ctrl.Antecedent(np.linspace(0, 1, 101), 'iteration')
alpha = ctrl.Consequent(np.linspace(0, 1, 101), 'alpha')

diversity['H'] = fuzz.trimf(diversity.universe, [0.0, 0.0, 0.25])
diversity['HM'] = fuzz.trimf(diversity.universe, [0.0, 0.25, 0.5])
diversity['M'] = fuzz.trimf(diversity.universe, [0.25, 0.5, 0.75])
diversity['LM'] = fuzz.trimf(diversity.universe, [0.5, 0.75, 1.0])
diversity['L'] = fuzz.trimf(diversity.universe, [0.75, 1.0, 1.0])

iteration['L'] = fuzz.trimf(iteration.universe, [0.0, 0.0, 0.25])
iteration['LM'] = fuzz.trimf(iteration.universe, [0.0, 0.25, 0.5])
iteration['M'] = fuzz.trimf(iteration.universe, [0.25, 0.5, 0.75])
iteration['HM'] = fuzz.trimf(iteration.universe, [0.5, 0.75, 1.0])
iteration['H'] = fuzz.trimf(iteration.universe, [0.75, 1.0, 1.0])

alpha['L'] = fuzz.trimf(alpha.universe, [0, 0, 0.25])
alpha['LM'] = fuzz.trimf(alpha.universe, [0, 0.25, 0.5])
alpha['M'] = fuzz.trimf(alpha.universe, [0.25, 0.5, 0.75])
alpha['HM'] = fuzz.trimf(alpha.universe, [0.5, 0.75, 1.0])
alpha['H'] = fuzz.trimf(alpha.universe, [0.75, 1.0, 1.0])

rule1 = ctrl.Rule(diversity['L'] & iteration['L'], alpha['M'])
rule2 = ctrl.Rule(diversity['L'] & iteration['LM'], alpha['M'])
rule3 = ctrl.Rule(diversity['L'] & iteration['M'], alpha['HM'])
rule4 = ctrl.Rule(diversity['L'] & iteration['HM'], alpha['H'])
rule5 = ctrl.Rule(diversity['L'] & iteration['H'], alpha['H'])

rule6 = ctrl.Rule(diversity['LM'] & iteration['L'], alpha['M'])
rule7 = ctrl.Rule(diversity['LM'] & iteration['LM'], alpha['M'])
rule8 = ctrl.Rule(diversity['LM'] & iteration['M'], alpha['M'])
rule9 = ctrl.Rule(diversity['LM'] & iteration['HM'], alpha['HM'])
rule10 = ctrl.Rule(diversity['LM'] & iteration['H'], alpha['H'])

rule11 = ctrl.Rule(diversity['M'] & iteration['L'], alpha['LM'])
rule12 = ctrl.Rule(diversity['M'] & iteration['LM'], alpha['M'])
rule13 = ctrl.Rule(diversity['M'] & iteration['M'], alpha['M'])
rule14 = ctrl.Rule(diversity['M'] & iteration['HM'], alpha['M'])
rule15 = ctrl.Rule(diversity['M'] & iteration['H'], alpha['HM'])

rule16 = ctrl.Rule(diversity['HM'] & iteration['L'], alpha['L'])
rule17 = ctrl.Rule(diversity['HM'] & iteration['LM'], alpha['LM'])
rule18 = ctrl.Rule(diversity['HM'] & iteration['M'], alpha['M'])
rule19 = ctrl.Rule(diversity['HM'] & iteration['HM'], alpha['M'])
rule20 = ctrl.Rule(diversity['HM'] & iteration['H'], alpha['M'])

rule21 = ctrl.Rule(diversity['H'] & iteration['L'], alpha['L'])
rule22 = ctrl.Rule(diversity['H'] & iteration['LM'], alpha['L'])
rule23 = ctrl.Rule(diversity['H'] & iteration['M'], alpha['LM'])
rule24 = ctrl.Rule(diversity['H'] & iteration['HM'], alpha['M'])
rule25 = ctrl.Rule(diversity['H'] & iteration['H'], alpha['M'])

alpha_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
     rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25])
selection_sim = ctrl.ControlSystemSimulation(alpha_ctrl)


def cvrp_fitness(chromosome):
    tour = chromosome.getInternalList()
    total_dist = 0.0
    current_load = 0
    last_node = DEPOT_INDEX

    for node in tour:
        node_demand = DEMANDS.get(node, 0)

        # Capacity control
        if current_load + node_demand > CAPACITY:
            total_dist += DIST_MATRIX[(last_node, DEPOT_INDEX)]
            total_dist += DIST_MATRIX[(DEPOT_INDEX, node)]
            current_load = node_demand
        else:
            total_dist += DIST_MATRIX[(last_node, node)]
            current_load += node_demand
        last_node = node

    # Back to depot from last city
    total_dist += DIST_MATRIX[(last_node, DEPOT_INDEX)]
    return total_dist

def hamming_distance(ind1, ind2):
    return sum(g1 != g2 for g1, g2 in zip(ind1, ind2))


def population_diversity(population):
    n = len(population)
    if n < 2:
        return 0.0

    distances = []

    for ind1, ind2 in combinations(population, 2):
        dist = hamming_distance(ind1.genomeList, ind2.genomeList)
        distances.append(dist)

    average_distance = sum(distances) / len(distances)
    PD_min = min(distances)
    PD_max = max(distances)

    if PD_max == PD_min:
        return 0.0

    normalized_diversity = (average_distance - PD_min) / (PD_max - PD_min)
    return normalized_diversity


def calculate_alpha(strategy, iteration, population, best, max_iter=GENERATION_COUNT):
    global alpha_history
    global Q_table, prev_state, prev_action
    global rewards, counts

    if strategy == "deterministic":
        # Increasing alpha linearly depending on iteration
        return 0.1 + 0.8 * (iteration / max_iter)



    elif strategy == "fuzzy":
        diversity_score = population_diversity(population)

        # For zero division and restrictions
        if diversity_score == 0.0:
            diversity_score = 1.0

        # Fuzzy inputs
        selection_sim.input['diversity'] = 1 - diversity_score
        selection_sim.input['iteration'] = iteration / max_iter
        selection_sim.compute()

        # Fuzzy output
        return selection_sim.output['alpha']



    elif strategy == "entropy":

        # Position-based entropy calculation
        matris = np.array([ind.genomeList for ind in population])
        entropies = []
        for i in range(matris.shape[1]):
            _, counts = np.unique(matris[:, i], return_counts=True)
            entropies.append(entropy(counts,base=2))
        ent = np.mean(entropies)

        # normalize
        return max(0.1, min(1.0, ent))

    elif strategy == "adaptive":

        if iteration == 0:
            alpha_history = [0.5]
            return 0.5

        # History weight
        gamma = 0.9
        improvement = (LAST_SCORE - best.getRawScore()) / 1000.0
        delta = max(-0.05, min(0.05, improvement))
        new_alpha = gamma * alpha_history[-1] + (1 - gamma) * (alpha_history[-1] + delta)
        new_alpha = min(1.0, max(0.0, new_alpha))

        alpha_history.append(new_alpha)
        return new_alpha



    elif strategy == "selfadaptive":
        # Average of individual alpha values
        return np.mean([getattr(ind, 'alpha', 0.5) for ind in population])

    if strategy == "qlearning":
        diversity_score = population_diversity(population)
        diversity_bin = int((1 - diversity_score) * 4)
        iteration_bin = int((iteration / max_iter) * 4)

        # ε-greedy selection
        epsilon = 0.1
        if random.random() < epsilon:
            action = random.randint(0, 4)
        else:
            action = np.argmax(Q_table[diversity_bin, iteration_bin])

        # alpha_bins = [0.1, 0.3, 0.5, 0.7, 0.9]
        alpha = alpha_bins[action]

        # Reward calculation
        if LAST_SCORE < 0:
            reward = 0
        else:
            raw_reward = LAST_SCORE - best.getRawScore()
            reward = max(0.0, raw_reward / max(1.0, abs(LAST_SCORE)))  # normalize

        # Update Q-table
        Q_table[prev_state[0], prev_state[1], prev_action] += 0.1 * (
                reward + 0.9 * np.max(Q_table[diversity_bin, iteration_bin]) -
                Q_table[prev_state[0], prev_state[1], prev_action]
        )

        prev_state = (diversity_bin, iteration_bin)
        prev_action = action

        return alpha

    elif strategy == "bandit":

        # For alphas that will be tested for the first time
        for i in range(len(alpha_bins)):
            if counts[i] == 0:
                counts[i] += 1
                return alpha_bins[i]

        total = sum(counts)
        ucb_values = [
            rewards[i] / counts[i] + math.sqrt(2 * math.log(total) / counts[i])
            for i in range(len(alpha_bins))
        ]

        idx = np.argmax(ucb_values)
        alpha = alpha_bins[idx]

        # Reward calculation (limit negative reward to a very small negative value)
        reward = LAST_SCORE - best.getRawScore()
        reward = max(-10, min(1000, reward))  # Limit negative reward to -10

        rewards[idx] += reward
        counts[idx] += 1

        #periodic reset
        if iteration == max_iter - 1:
            rewards = [0.0] * len(alpha_bins)
            counts = [0] * len(alpha_bins)

        return alpha
    else:
        # Default fallback
        return 0.5

def mutate_alpha(individual, sigma=0.05):
    if not hasattr(individual, 'alpha'):
        individual.alpha = 0.5
    individual.alpha += random.gauss(0, sigma)
    individual.alpha = max(0.0, min(1.0, individual.alpha))
def self_adaptive_mutator(genome, **args):
    # Apply existing mutation
    G1DListMutatorDisplacement(genome, **args)
    # also mutate alpha
    mutate_alpha(genome)
    return 1


def evolve_callback(ga_engine):
    global LAST_SCORE
    curr_gen = ga_engine.getCurrentGeneration()
    best = ga_engine.bestIndividual()

    alpha_val = calculate_alpha(strategy, curr_gen, ga_engine.internalPop, best)

    if alpha_val < 0.7:
        ga_engine.selector.set(dict_selector_operators["EEBS"])
    elif 0.7 < alpha_val < 0.8:
        ga_engine.selector.set(dict_selector_operators["NTS"])
    elif 0.8 < alpha_val < 1:
        ga_engine.selector.set(dict_selector_operators["FPS"])

    f.write(f"{best.getRawScore()}\n")


    LAST_SCORE = best.getRawScore()
    return False


def main_run(crossover_func, problemname):
    global DIST_MATRIX, DEMANDS, CAPACITY, CITIES_COUNT, DEPOT_INDEX

    path = os.path.join(os.path.dirname(__file__), f"vrp_datasets/small/{problemname}.vrp")
    problem = tsplib95.load(path)

    CAPACITY = problem.capacity
    original_nodes = list(problem.get_nodes())
    CITIES_COUNT = len(original_nodes)

    DIST_MATRIX.clear()
    DEMANDS.clear()
    DEPOT_INDEX = 0

    for i in range(CITIES_COUNT):
        orig_i = original_nodes[i]
        DEMANDS[i] = problem.demands.get(orig_i, 0)
        for j in range(CITIES_COUNT):
            orig_j = original_nodes[j]
            DIST_MATRIX[(i, j)] = float(problem.get_weight(orig_i, orig_j))


    customers = [n for n in range(CITIES_COUNT) if n != DEPOT_INDEX]
    genome = G1DList.G1DList(len(customers))
    genome.setInternalList(customers)

    genome.evaluator.set(cvrp_fitness)
    genome.crossover.set(crossover_func)
    genome.mutator.set(G1DListMutatorDisplacement)
    #genome.mutator.set(self_adaptive_mutator)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(GENERATION_COUNT)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)
    ga.stepCallback.set(evolve_callback)

    start = time.time()
    ga.evolve(freq_stats=1)
    end = time.time()

    f.write(str(end - start) + "\n")


if __name__ == "__main__":

    methods = ["PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "GX", "IGX", "SCX"]

    for m in range(0, len(methods)):

        current_base_seed = 1000

        for i in range(1, 31):
            # Argparse kurulumu
            parser = argparse.ArgumentParser(description='Crossover and CVRP problems')
            parser.add_argument('--crossover', help="Crossover operator to use", default=methods[m])
            parser.add_argument('--problemname', help="CVRP problem filename", default='A-n33-k5')

            current_base_seed += 1
            parser.add_argument('--randomseed', help="Random seed to use", default=current_base_seed, type=int)
            args, unknown = parser.parse_known_args()

            crossover_operator_name = args.crossover
            randomseed = args.randomseed
            problemname = args.problemname

            random.seed(randomseed)
            np.random.seed(randomseed)

            if crossover_operator_name not in dict_crossoever_operators:
                raise ValueError(f"{crossover_operator_name} is not in dict_crossoever_operators")

            crossover_operator_func = dict_crossoever_operators[crossover_operator_name]

            print( f"--- Experiment has been started: {crossover_operator_name} | Problem: {problemname} | Seed: {randomseed} | Strategy: {strategy} ---")

            f = open(f"{crossover_operator_name}_{problemname}_Experiment_{randomseed}_{strategy}.txt", "w")

            try:
                main_run(crossover_operator_func, problemname)
            finally:
                f.close()