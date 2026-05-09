import argparse
import collections
import math
import os
import random

from math import sqrt



from pyevolve import Consts
from pyevolve import GSimpleGA
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve.representations import G1DList
from pyevolve.selections import SelectionRank

collections.Callable = collections.abc.Callable



LAST_SCORE = -1


from helper_tsp import run_tsp_coordinate_cities, tour_length_xy, evolve_callback_xy
from helper_tsp import dict_crossoever_operators, get_coordinates_for_tsp_problem



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

            coordinates = get_coordinates_for_tsp_problem(problemname)
            experiment_name = f"{problemname}-{crossover_operator_name}-{randomseed}"
            run_tsp_coordinate_cities( experiment_name=experiment_name
                                      , coordinates = coordinates
                                      , selection_method=SelectionRank.SelectorExplorationExploitationBalance
                                    )
