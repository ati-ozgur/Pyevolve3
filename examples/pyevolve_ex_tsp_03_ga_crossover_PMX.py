from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverPMX
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom

from helper_tsp import run_tsp

if __name__ == "__main__":

    run_tsp( problem_name="tsp_random_cities_CrossoverPMX"
            , crossover_method=G1DListCrossoverPMX
            , mutation_method=G1DListMutatorDisplacement
            , initialization_method=G1DListTSPInitializatorRandom
            )
