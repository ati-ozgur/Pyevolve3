import math
import os
import random

from pyevolve.representations import G1DList
from pyevolve import GSimpleGA
from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverEdge
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve import Consts
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom



PIL_SUPPORT = None
LAST_SCORE = -1



try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_SUPPORT = True
except ImportError:
    PIL_SUPPORT = False


def get_cartesian_matrix(coords):
    """ A distance matrix """
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = math.sqrt(dx * dx + dy * dy)
            matrix[i, j] = dist
    return matrix


def tour_length_xy(matrix, tour, cities):
    """ Returns the total length of the tour """
    total = 0
    t = tour.getInternalList()
    for i in range(cities):
        j = (i + 1) % cities
        total += matrix[t[i], t[j]]
    return total


def write_tour_to_img(coords, tour, img_file, max_generation_count):
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
    print(f"The plot was saved into the {img_file} file. max generation: {max_generation_count}")

# This is to make a video of best individuals along the evolution
# see create_video_from_images.bash for example ffmpeg commands.

def evolve_callback_xy(ga_engine):
    global LAST_SCORE
    max_generation_count = ga_engine.getGenerations()
    filename_digit_count = int(math.floor(math.log10(max_generation_count))) +1
    current_generation = ga_engine.getCurrentGeneration()

    results_directory = ga_engine.getParam("results_directory")
    if results_directory is None:
        raise ValueError("results_directory parameter is not set in the GA engine parameters")  
    
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    coordinates = ga_engine.getParam("coordinates")
    if coordinates is None:
        raise ValueError("coordinates parameter is not set in the GA engine parameters")

    if current_generation % 100 == 0:
        best = ga_engine.bestIndividual()
        if LAST_SCORE != best.getRawScore():
            filename = f"{results_directory}/tsp_result_{current_generation:0{filename_digit_count}}.png"
            write_tour_to_img(coordinates, best, filename,max_generation_count)
            LAST_SCORE = best.getRawScore()
    return False

def run_tsp(width=1024, height=768
             , cities_count=100
             , max_generation_count=2000
             , crossover_rate=1.0
             , mutation_rate=0.02
             , population_size=80
             , crossover_method=None
             , mutation_method=None
             , selection_method=None
             , initialization_method=None
             , results_directory="tspimg"
             , random_seed=1024):

    random.seed(random_seed)
    coordinates = [(random.randint(0, width), random.randint(0, height))
              for i in range(cities_count)]
    cm = get_cartesian_matrix(coordinates)
    genome = G1DList.G1DList(len(coordinates))

    genome.evaluator.set(lambda chromosome: tour_length_xy(cm, chromosome, cities_count))
    if crossover_method is not None:
        genome.crossover.set(crossover_method)
    else:
        genome.crossover.set(G1DListCrossoverEdge)
    if mutation_method is not None:
        genome.mutator.set(mutation_method)
    else:
        genome.mutator.set(G1DListMutatorSwap)
    if initialization_method is not None:
        genome.initializator.set(initialization_method)
    else:
        genome.initializator.set(G1DListTSPInitializatorRandom)



    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(max_generation_count)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(crossover_rate)
    ga.setMutationRate(mutation_rate)
    ga.setPopulationSize(population_size)

    if selection_method is not None:
        ga.selector.set(selection_method)

    ga.setParams(results_directory=results_directory)
    ga.setParams(coordinates=coordinates)

    if PIL_SUPPORT:
        ga.stepCallback.set(  evolve_callback_xy)

    ga.evolve(freq_stats=500)
    best = ga.bestIndividual()

    if PIL_SUPPORT:
        img_filename = f"{results_directory}/tsp_result.png"
        write_tour_to_img(coordinates, best, img_filename,max_generation_count)
    else:
        print("No PIL detected, cannot plot the graph !")
