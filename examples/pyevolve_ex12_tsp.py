
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
CITIES_COUNT = 100
WIDTH = 1024
HEIGHT = 768

RESULTS_DIRECTORY = "tspimg"
MAX_GENERATION_COUNT = 2000




from helper_tsp import PIL_SUPPORT, cartesian_matrix, evolve_callback_xy, tour_length_xy, write_tour_to_img


def main_run():
    global cm, coordinates, WIDTH, HEIGHT

    coordinates = [(random.randint(0, WIDTH), random.randint(0, HEIGHT))
              for i in range(CITIES_COUNT)]
    cm = cartesian_matrix(coordinates)
    genome = G1DList.G1DList(len(coordinates))

    genome.evaluator.set(lambda chromosome: tour_length_xy(cm, chromosome, CITIES_COUNT))
    genome.crossover.set(G1DListCrossoverEdge)
    genome.mutator.set(G1DListMutatorSwap)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    # 3662.69
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(MAX_GENERATION_COUNT)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)

    ga.setParams(results_directory=RESULTS_DIRECTORY)
    ga.setParams(coordinates=coordinates)

    if PIL_SUPPORT:
        ga.stepCallback.set(  evolve_callback_xy)

    ga.evolve(freq_stats=500)
    best = ga.bestIndividual()

    if PIL_SUPPORT:
        write_tour_to_img(coordinates, best, f"{RESULTS_DIRECTORY}/tsp_result.png",MAX_GENERATION_COUNT)
    else:
        print("No PIL detected, cannot plot the graph !")


if __name__ == "__main__":
    main_run()
