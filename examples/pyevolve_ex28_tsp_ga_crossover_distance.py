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

from helper_tsp import dict_crossoever_operators, crossover_methods, get_distance_matrixes_from_tsp_problem,tour_length



LAST_SCORE = -1

RESULTS_DIRECTORY = "tspimg"
GENERATION_COUNT = 1001
filename_digit_count = int(math.floor(math.log10(GENERATION_COUNT))) + 1








# This is to make a video of best individuals along the evolution
# see create_video_from_images.bash for example ffmpeg commands.

def evolve_callback(ga_engine):
    global LAST_SCORE
    current_generation = ga_engine.getCurrentGeneration()
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    if current_generation % 1 == 0:
        best = ga_engine.bestIndividual()
        if LAST_SCORE < best.getRawScore():
            best_raw_score = best.getRawScore()
            f.write(f"current_generation:{current_generation},best_raw_score:{best_raw_score}\n")

    return False


def main_run(crossover_operator_func, problemname):

    distance_matrix_dict, distance_matrix_list = get_distance_matrixes_from_tsp_problem(problemname)

    cities_count = len(distance_matrix_list)
    genome = G1DList.G1DList(cities_count)

    genome.setParams(
        distance_matrix_dict=distance_matrix_dict,
        distance_matrix_list=distance_matrix_list,
    )

    genome.evaluator.set(
        lambda chromosome: tour_length(distance_matrix_dict, chromosome, cities_count)
    )
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
    time_elapsed = end-start
    print("time_elapsed",time_elapsed)
    f.write(f"time_elapsed:{time_elapsed}\n")



if __name__ == "__main__":
    
    for m in range(0, len(crossover_methods)):
        randomseed = 1000
        for i in range(1, 31):
            parser = argparse.ArgumentParser(description='crossover, tsp problems')
            parser.add_argument('--crossover', help="cross over operator to use", default=crossover_methods[m])
            parser.add_argument('--problemname', help="TSP problem filename", default='gr21')
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
