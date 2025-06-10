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

cm = []
coords = []
CITIES = None
LAST_SCORE = -1

RESULTS_DIRECTORY = "tspimg"
GENERATION_COUNT = 1001
filename_digit_count = int(math.floor(math.log10(GENERATION_COUNT))) + 1

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

        diversity = population_diversity(ga_engine.internalPop)

        if diversity == 0:
            diversity = 1.0

        selection_sim.input['diversity'] = 1 - diversity
        selection_sim.input['iteration'] = current_generation / GENERATION_COUNT
        selection_sim.compute()

        alpha = selection_sim.output['alpha']

        if alpha < 0.7:
            ga_engine.selector.set(dict_selector_operators["EEBS"])

        elif 0.7 < alpha < 0.8:
            ga_engine.selector.set(dict_selector_operators["NTS"])

        elif 0.8 < alpha < 1:
            ga_engine.selector.set(dict_selector_operators["FPS"])

        if LAST_SCORE != best.getRawScore():
            f.write(str(best.getRawScore()) + "\n")
            filename = f"{RESULTS_DIRECTORY}/tsp_result_{current_generation:0{filename_digit_count}}.png"
            # write_tour_to_img(coords, best, filename )

    return False


def main_run(crossover_operator_func, problemname):
    global cm, coords, WIDTH, HEIGHT, CITIES
    filename = 'data/' + problemname + '.tsp'
    path = os.path.join(os.path.dirname(__file__), filename)
    problem = tsplib95.load(path)
    print(list(problem.get_nodes()))

    coords = [tuple(problem.node_coords[i]) for i in range(1, len(list(problem.get_nodes())) + 1)]
    CITIES = len(list(problem.get_nodes()))
    cm = cartesian_matrix(coords)
    genome = G1DList.G1DList(len(coords))

    genome.setParams(dist=cm)
    genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome))
    genome.crossover.set(crossover_operator_func)
    genome.mutator.set(G1DListMutatorDisplacement)
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
        write_tour_to_img(coords, best, f"{RESULTS_DIRECTORY}/tsp_result.png")
    else:
        print("No PIL detected, cannot plot the graph !")


if __name__ == "__main__":
    methods = ["PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "GX", "IGX", "SCX"]
for m in range(0, len(methods)):
    randomseed = 1000
    for i in range(1, 31):
        parser = argparse.ArgumentParser(description='crossover, tsp problems')
        parser.add_argument('--crossover', help="cross over operator to use", default=methods[m])
        parser.add_argument('--problemname', help="TSP problem filename", default='att532')
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
        f = open(crossover_operator_name + "_" + problemname + "_" + "Experiment_" + str(randomseed) + ".txt", "w")
        main_run(crossover_operator_func, problemname)
