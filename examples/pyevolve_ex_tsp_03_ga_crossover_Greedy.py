
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverGreedy
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom

from helper_tsp import run_tsp

if __name__ == "__main__":


    run_tsp(problem_name="tsp_random_cities_CrossoverGreedy"
            , crossover_method=G1DListCrossoverGreedy
            , mutation_method=G1DListMutatorDisplacement
            , initialization_method=G1DListTSPInitializatorRandom
            )

