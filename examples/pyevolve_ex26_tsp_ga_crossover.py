from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverIGX
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom

from helper_tsp import run_tsp

if __name__ == "__main__":


    run_tsp( experiment_name="tsp_crossoverIGX"
            , crossover_method=G1DListCrossoverIGX
            , mutation_method=G1DListMutatorDisplacement
            , initialization_method=G1DListTSPInitializatorRandom
            , cities_count=8
            )
