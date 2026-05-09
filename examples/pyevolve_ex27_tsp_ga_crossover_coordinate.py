import argparse
import collections
import math
import os
import random
import time
from math import sqrt

import tsplib95

from pyevolve import Consts
from pyevolve import GSimpleGA
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverPMX, G1DListCrossoverOX, \
    G1DListCrossoverOX2, G1DListCrossoverCycle, G1DListCrossoverPOS, G1DListCrossoverMPX, G1DListCrossoverEdge, \
    G1DListCrossoverEPMX, G1DListCrossoverGreedy, G1DListCrossoverIGX, G1DListCrossoverSequentialConstructive
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve.representations import G1DList
from pyevolve.selections import SelectionRank

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





def evolve_callback(ga_engine):
    global LAST_SCORE
    current_generation = ga_engine.getCurrentGeneration()
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    if current_generation % 1 == 0:
        best = ga_engine.bestIndividual()
        if LAST_SCORE != best.getRawScore():
            pass
            #f.write(str(best.getRawScore()) + "\n")
            filename = f"{RESULTS_DIRECTORY}/tsp_result_{current_generation:0{filename_digit_count}}.png"

    return False


def main_run(crossover_operator_func, problemname):
    global cm, coords, WIDTH, HEIGHT, CITIES
    filename = 'tsp_datasets/' + problemname + '.tsp'
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
    genome.mutator.set(G1DListMutatorSwap)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    # 3662.69
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(GENERATION_COUNT)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)
    ga.selector.set(SelectionRank.SelectorExplorationExploitationBalance)

    ga.stepCallback.set(evolve_callback)
    # 21666.49
    start = time.time()
    ga.evolve(freq_stats=1)
    end = time.time()
    best = ga.bestIndividual()
    print(end - start)
    #f.write(str(end - start) + "\n")

    if PIL_SUPPORT:
        write_tour_to_img(coords, best, f"{RESULTS_DIRECTORY}/tsp_result.png")
    else:
        print("No PIL detected, cannot plot the graph !")


if __name__ == "__main__":
    methods = ["PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "GX", "IGX", "SCX"]
    for m in range(0, len(methods)):
        randomseed = 1000
        for i in range(1, 2):
            parser = argparse.ArgumentParser(description='crossover, tsp problems')
            parser.add_argument('--crossover', help="cross over operator to use", default=methods[m])
            parser.add_argument('--problemname', help="TSP problem filename", default='eil51')
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
            #f = open(crossover_operator_name + "_" + problemname + "_" + "Experiment_" + str(randomseed) + ".txt", "w")
            main_run(crossover_operator_func, problemname)
