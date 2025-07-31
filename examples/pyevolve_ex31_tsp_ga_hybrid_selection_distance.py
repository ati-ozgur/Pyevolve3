import argparse
import collections
import math
import os
import random
import time
from itertools import combinations
from math import sqrt

import numpy as np
import skfuzzy as fuzz
import tsplib95
from scipy.stats import entropy
from skfuzzy import control as ctrl

from pyevolve import Consts
from pyevolve import GSimpleGA
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverPMX, G1DListCrossoverOX, \
    G1DListCrossoverOX2, G1DListCrossoverCycle, G1DListCrossoverPOS, G1DListCrossoverMPX, G1DListCrossoverEdge, \
    G1DListCrossoverEPMX, G1DListCrossoverGreedy, G1DListCrossoverIGX, G1DListCrossoverSequentialConstructive
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.representations import G1DList
from pyevolve.selections.SelectionRank import SelectorFitnessProportional, SelectorLinearRanking, \
    SelectorExponentialRanking, SelectorSplitRanking, SelectorExplorationExploitationBalance, SelectorNewTournament
from pyevolve.selections.Selectors import GTournamentSelector

collections.Callable = collections.abc.Callable

dict_crossoever_operators = {
    "PMX": G1DListCrossoverPMX,
    "OX": G1DListCrossoverOX,
    "OX2": G1DListCrossoverOX2,
    "CX": G1DListCrossoverCycle,
    "POS": G1DListCrossoverPOS,
    "MPX": G1DListCrossoverMPX,
    "ERX": G1DListCrossoverEdge,
    "EPMX": G1DListCrossoverEPMX,
    "GX": G1DListCrossoverGreedy,
    "IGX": G1DListCrossoverIGX,
    "SCX": G1DListCrossoverSequentialConstructive
}

dict_selector_operators = {
    "FPS": SelectorFitnessProportional,
    "LRS": SelectorLinearRanking,
    "ERS": SelectorExponentialRanking,
    "EEBS": SelectorExplorationExploitationBalance,
    "SRS": SelectorSplitRanking,
    "NTS": SelectorNewTournament,
    "TS": GTournamentSelector,
}

PIL_SUPPORT = None

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_SUPPORT = True
except ImportError:
    PIL_SUPPORT = False

cm = {}
coords = []
CITIES = None
LAST_SCORE = -1

RESULTS_DIRECTORY = "tspimg"
GENERATION_COUNT = 1001
filename_digit_count = int(math.floor(math.log10(GENERATION_COUNT))) + 1

strategy="deterministic"
#strategy="fuzzy"
#strategy="entropy"
#strategy="adaptive"
#strategy="selfadaptive"
#strategy="qlearning"
#strategy="bandit"


Q_table = np.zeros((5, 5, 5))  # (diversity_bin, iteration_bin, alpha_bin)
prev_state = (0, 0)
prev_action = 2  # middle alpha bin
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


def cartesian_matrix(coords):
    """ A distance matrix """
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            matrix[i, j] = dist
    return matrix


def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    total = 0
    t = tour.getInternalList()
    for i in range(CITIES):
        j = (i + 1) % CITIES
        total += matrix[t[i], t[j]]
    return total


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

def write_tour_to_img(coords, tour, img_file):
    """ The function to plot the graph """
    padding = 20
    coords = [(x + padding, y + padding) for (x, y) in coords]
    maxx, maxy = 0, 0
    for x, y in coords:
        maxx, maxy = max(x, maxx), max(y, maxy)
    maxx += padding
    maxy += padding
    img = Image.new("RGB", (int(maxx), int(maxy)), color=(255, 255, 255))
    font = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        x1, y1 = coords[city_i]
        x2, y2 = coords[city_j]
        d.line((int(x1), int(y1), int(x2), int(y2)), fill=(0, 0, 0))
        d.text((int(x1) + 7, int(y1) - 5), str(i), font=font, fill=(32, 32, 32))

    for x, y in coords:
        x, y = int(x), int(y)
        d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0), fill=(196, 196, 196))
    del d
    img.save(img_file, "PNG")
    print(f"The plot was saved into the {img_file} file. max generation: {GENERATION_COUNT}")


# This is to make a video of best individuals along the evolution
# Use mencoder to create a video with the file list list.txt
# mencoder mf://@list.txt -mf w=400:h=200:fps=3:type=png -ovc lavc
#          -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o output.avi
#
def evolve_callback(ga_engine):
    global LAST_SCORE
    current_generation = ga_engine.getCurrentGeneration()
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    if current_generation % 1 == 0:
        best = ga_engine.bestIndividual()

        alpha = calculate_alpha(strategy, current_generation, ga_engine.internalPop, ga_engine.bestIndividual())

        if alpha < 0.7:
            ga_engine.selector.set(dict_selector_operators["EEBS"])

        elif 0.7 < alpha < 0.8:
            ga_engine.selector.set(dict_selector_operators["NTS"])

        elif 0.8 < alpha < 1:
            ga_engine.selector.set(dict_selector_operators["FPS"])

        f.write(str(best.getRawScore()) + "\n")

        if LAST_SCORE != best.getRawScore():
            LAST_SCORE = best.getRawScore()
            filename = f"{RESULTS_DIRECTORY}/tsp_result_{current_generation:0{filename_digit_count}}.png"
            # write_tour_to_img(coords, best, filename )

    return False
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

def main_run(crossover_operator_func, problemname):
    global cm, coords, WIDTH, HEIGHT, CITIES
    filename = 'data/' + problemname + '.tsp'
    path = os.path.join(os.path.dirname(__file__), filename)
    problem = tsplib95.load(path)
    print(list(problem.get_nodes()))

    CITIES = len(list(problem.get_nodes()))
    for i in range(0, CITIES):
        for j in range(0, CITIES):
            edge = i, j
            weight = problem.get_weight(*edge)
            cm[i, j] = weight

    genome = G1DList.G1DList(CITIES)

    genome.setParams(dist=cm)
    genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome))
    genome.crossover.set(crossover_operator_func)
    genome.mutator.set(G1DListMutatorDisplacement)
    #genome.mutator.set(self_adaptive_mutator)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    # 3662.69
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(GENERATION_COUNT)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)
    ga.selector.set(dict_selector_operators["EEBS"])

    ga.stepCallback.set(evolve_callback)
    # 21666.49
    start = time.time()
    ga.evolve(freq_stats=1)
    end = time.time()
    best = ga.bestIndividual()
    print(end - start)
    f.write(str(end - start) + "\n")

    if PIL_SUPPORT:
        # write_tour_to_img(coords, best, f"{RESULTS_DIRECTORY}/tsp_result.png")
        print("PIL detected, cannot plot the graph !")
    else:
        print("No PIL detected, cannot plot the graph !")


if __name__ == "__main__":
    methods = ["PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "GX", "IGX", "SCX"]
for m in range(0, len(methods)):
    randomseed = 1000
    for i in range(1, 31):
        parser = argparse.ArgumentParser(description='crossover, tsp problems')
        parser.add_argument('--crossover', help="cross over operator to use", default=methods[m])
        parser.add_argument('--problemname', help="TSP problem filename", default='br17')
        randomseed = randomseed + 1
        parser.add_argument('--randomseed', help="random seed to use", default=randomseed, type=int)
        args = parser.parse_args()
        crossover_operator_name = args.crossover
        randomseed = args.randomseed
        random.seed(randomseed)
        problemname = args.problemname
        if crossover_operator_name not in dict_crossoever_operators:
            raise ValueError(crossover_operator_name + 'is not in dict_crossoever_operators')
        else:
            crossover_operator_func = dict_crossoever_operators[crossover_operator_name]

        print(args)
        f = open(crossover_operator_name + "_" + problemname + "_" + "Experiment_" + str(randomseed) +"_"+strategy+".txt", "w")
        main_run(crossover_operator_func, problemname)
