import argparse
import collections
import math
import os
import random
import time
from math import sqrt



from pyevolve import Consts
from pyevolve import GSimpleGA
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve.representations import G1DList
from pyevolve.selections import SelectionRank

collections.Callable = collections.abc.Callable



LAST_SCORE = -1


from helper_tsp import get_distance_matrixes, tour_length_xy, evolve_callback_xy
from helper_tsp import dict_crossoever_operators, get_coordinates_for_tsp_problem



def main_run(crossover_operator_func
    , problemname
    , results_directory="tspimg"
    , generation_count = 1001
    ):
    experiment_name = problemname
    coordinates = get_coordinates_for_tsp_problem(problemname)
    cities_count = len(coordinates)
    distance_matrix_dict, distance_matrix_list = get_distance_matrixes(coordinates)
    genome = G1DList.G1DList(cities_count)

    genome.setParams(distance_matrix_dict=distance_matrix_dict, distance_matrix_list=distance_matrix_list)

    genome.evaluator.set(lambda chromosome: tour_length_xy(distance_matrix_dict, chromosome, cities_count))

    genome.crossover.set(crossover_operator_func)
    genome.mutator.set(G1DListMutatorSwap)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    # 3662.69
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(generation_count)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)
    ga.selector.set(SelectionRank.SelectorExplorationExploitationBalance)

    ga.setParams(results_directory=results_directory)
    ga.setParams(coordinates=coordinates)
    ga.setParams(experiment_name=experiment_name)


    ga.stepCallback.set(evolve_callback_xy)
    # 21666.49
    start = time.time()
    ga.evolve(freq_stats=1)
    end = time.time()
    best = ga.bestIndividual()
    print(end - start)
    #f.write(str(end - start) + "\n")



if __name__ == "__main__":
    methods = ["GX", "IGX","PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "SCX"]
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
