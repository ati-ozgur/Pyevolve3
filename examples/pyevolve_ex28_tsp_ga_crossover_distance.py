from math import sqrt

import random
import math
import tsplib95
import os

from pyevolve.representations import G1DList
from pyevolve import GSimpleGA
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverPMX
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve import Consts
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.selections import SelectionRank
import collections
collections.Callable = collections.abc.Callable

random.seed(1024)

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
GENERATION_COUNT = 200000
filename_digit_count = int(math.floor(math.log10(GENERATION_COUNT))) +1


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

    if current_generation % 100 == 0:
        best = ga_engine.bestIndividual()
        if LAST_SCORE != best.getRawScore():
            filename = f"{RESULTS_DIRECTORY}/tsp_result_{current_generation:0{filename_digit_count}}.png"
            #write_tour_to_img(coords, best, filename )

    return False


def main_run():
    global cm, coords, WIDTH, HEIGHT, CITIES
    path = os.path.join(os.path.dirname(__file__), 'data/fri26.tsp')
    problem = tsplib95.load(path)
    print(list(problem.get_nodes()))

    CITIES=len(list(problem.get_nodes()))
    for i in range(0,CITIES):
        for j in range(0, CITIES):
            edge=i,j
            weight= problem.get_weight(*edge)
            cm[i,j]=weight

    genome = G1DList.G1DList(CITIES)

    genome.setParams(dist=cm)
    genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome))
    genome.crossover.set(G1DListCrossoverPMX)
    genome.mutator.set(G1DListMutatorDisplacement)
    genome.initializator.set(G1DListTSPInitializatorRandom)

    # 3662.69
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(GENERATION_COUNT)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)
    ga.selector.set(SelectionRank.SelectorLinearRanking)

    # This is to make a video
    if PIL_SUPPORT:
        ga.stepCallback.set(evolve_callback)
    # 21666.49

    ga.evolve(freq_stats=1)
    best = ga.bestIndividual()

    if PIL_SUPPORT:
        write_tour_to_img(coords, best, f"{RESULTS_DIRECTORY}/tsp_result.png")
    else:
        print("No PIL detected, cannot plot the graph !")

if __name__ == "__main__":
    main_run()
