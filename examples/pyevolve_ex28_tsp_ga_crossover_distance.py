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

dict_crossoever_operators = {
    "PMX": G1DListCrossoverPMX,
    "OX": G1DListCrossoverOX,
    "OX2": G1DListCrossoverOX2,
    "CX": G1DListCrossoverCycle,
    "POS": G1DListCrossoverPOS,
    "MPX": G1DListCrossoverMPX,
    "ERX": G1DListCrossoverEdge,
    "EPMX": G1DListCrossoverEPMX,
    "GX": G1DListCrossoverGreedy,
    "IGX": G1DListCrossoverIGX,
    "SCX": G1DListCrossoverSequentialConstructive
}

PIL_SUPPORT = None

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_SUPPORT = True
except ImportError:
    PIL_SUPPORT = False

cm = {}
coords = []
CITIES = None
LAST_SCORE = -1

RESULTS_DIRECTORY = "tspimg"
GENERATION_COUNT = 1001
filename_digit_count = int(math.floor(math.log10(GENERATION_COUNT))) + 1


def cartesian_matrix(coords):
    """ A distance matrix """
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            matrix[i, j] = dist
    return matrix


def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    total = 0
    t = tour.getInternalList()
    for i in range(CITIES):
        j = (i + 1) % CITIES
        total += matrix[t[i], t[j]]
    return total


def write_tour_to_img(coords, tour, img_file):
    """ The function to plot the graph """
    padding = 20
    coords = [(x + padding, y + padding) for (x, y) in coords]
    maxx, maxy = 0, 0
    for x, y in coords:
        maxx, maxy = max(x, maxx), max(y, maxy)
    maxx += padding
    maxy += padding
    img = Image.new("RGB", (int(maxx), int(maxy)), color=(255, 255, 255))
    font = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        x1, y1 = coords[city_i]
        x2, y2 = coords[city_j]
        d.line((int(x1), int(y1), int(x2), int(y2)), fill=(0, 0, 0))
        d.text((int(x1) + 7, int(y1) - 5), str(i), font=font, fill=(32, 32, 32))

    for x, y in coords:
        x, y = int(x), int(y)
        d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0), fill=(196, 196, 196))
    del d
    img.save(img_file, "PNG")
    print(f"The plot was saved into the {img_file} file. max generation: {GENERATION_COUNT}")


# This is to make a video of best individuals along the evolution
# Use mencoder to create a video with the file list list.txt
# mencoder mf://@list.txt -mf w=400:h=200:fps=3:type=png -ovc lavc
#          -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o output.avi
#
def evolve_callback(ga_engine):
    global LAST_SCORE
    current_generation = ga_engine.getCurrentGeneration()
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    if current_generation % 1 == 0:
        best = ga_engine.bestIndividual()
        if LAST_SCORE != best.getRawScore():
            f.write(str(best.getRawScore()) + "\n")
            filename = f"{RESULTS_DIRECTORY}/tsp_result_{current_generation:0{filename_digit_count}}.png"
            # write_tour_to_img(coords, best, filename )

    return False


def main_run(crossover_operator_func, problemname):
    global cm, coords, WIDTH, HEIGHT, CITIES
    filename = 'data/' + problemname + '.tsp'
    path = os.path.join(os.path.dirname(__file__), filename)
    problem = tsplib95.load(path)
    print(list(problem.get_nodes()))

    CITIES = len(list(problem.get_nodes()))
    for i in range(0, CITIES):
        for j in range(0, CITIES):
            edge = i, j
            weight = problem.get_weight(*edge)
            cm[i, j] = weight

    genome = G1DList.G1DList(CITIES)

    genome.setParams(dist=cm)
    genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome))
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
    print(end - start)
    f.write(str(end - start) + "\n")

    if PIL_SUPPORT:
        # write_tour_to_img(coords, best, f"{RESULTS_DIRECTORY}/tsp_result.png")
        print("PIL detected, cannot plot the graph !")
    else:
        print("No PIL detected, cannot plot the graph !")


if __name__ == "__main__":
    methods = ["PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "GX", "IGX", "SCX"]
for m in range(0, len(methods)):
    randomseed = 1000
    for i in range(1, 31):
        parser = argparse.ArgumentParser(description='crossover, tsp problems')
        parser.add_argument('--crossover', help="cross over operator to use", default=methods[m])
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
