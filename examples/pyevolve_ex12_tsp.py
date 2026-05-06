
import random

from pyevolve.representations import G1DList
from pyevolve import GSimpleGA
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverEdge
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve import Consts
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom







from helper_tsp import PIL_SUPPORT, get_cartesian_matrix, evolve_callback_xy, tour_length_xy, write_tour_to_img


def run_tsp(width=1024, height=768
             , cities_count=100
             , max_generation_count=2000
             , crossover_rate=1.0
             , mutation_rate=0.02
             , population_size=80
             , results_directory="tspimg"
             , random_seed=1024):

    random.seed(random_seed)
    coordinates = [(random.randint(0, width), random.randint(0, height))
              for i in range(cities_count)]
    cm = get_cartesian_matrix(coordinates)
    genome = G1DList.G1DList(len(coordinates))

    genome.evaluator.set(lambda chromosome: tour_length_xy(cm, chromosome, cities_count))
    genome.crossover.set(G1DListCrossoverEdge)
    genome.mutator.set(G1DListMutatorSwap)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(max_generation_count)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(crossover_rate)
    ga.setMutationRate(mutation_rate)
    ga.setPopulationSize(population_size)

    ga.setParams(results_directory=results_directory)
    ga.setParams(coordinates=coordinates)

    if PIL_SUPPORT:
        ga.stepCallback.set(  evolve_callback_xy)

    ga.evolve(freq_stats=500)
    best = ga.bestIndividual()

    if PIL_SUPPORT:
        write_tour_to_img(coordinates, best, f"{results_directory}/tsp_result.png",max_generation_count)
    else:
        print("No PIL detected, cannot plot the graph !")


if __name__ == "__main__":
    run_tsp()
