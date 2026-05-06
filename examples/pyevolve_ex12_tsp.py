
import random
import math

from pyevolve.representations import G1DList
from pyevolve import GSimpleGA
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverEdge
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve import Consts
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom


random.seed(1024)


cm = []
coordinates = []




from helper_tsp import PIL_SUPPORT, cartesian_matrix, evolve_callback_xy, tour_length_xy, write_tour_to_img


def main_run(width=1024, height=768
             , cities_count=100
             , max_generation_count=2000
             , results_directory="tspimg"):

    global cm, coordinates, HEIGHT

    coordinates = [(random.randint(0, width), random.randint(0, height))
              for i in range(cities_count)]
    cm = cartesian_matrix(coordinates)
    genome = G1DList.G1DList(len(coordinates))

    genome.evaluator.set(lambda chromosome: tour_length_xy(cm, chromosome, cities_count))
    genome.crossover.set(G1DListCrossoverEdge)
    genome.mutator.set(G1DListMutatorSwap)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(max_generation_count)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)

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
    main_run()
