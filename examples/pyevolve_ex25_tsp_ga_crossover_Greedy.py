
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverGreedy
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom

from helper_tsp import run_tsp_random_coordinate_cities

if __name__ == "__main__":


    run_tsp_random_coordinate_cities( experiment_name="tsp_crossoverGreedy"
            , crossover_method=G1DListCrossoverGreedy
            , mutation_method=G1DListMutatorDisplacement
            , initialization_method=G1DListTSPInitializatorRandom
            )
