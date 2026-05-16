import math
import os
import random
import time

import tsplib95

from pyevolve.representations import G1DList
from pyevolve import GSimpleGA
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorSwap
from pyevolve import Consts
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom

from pyevolve.perturbations.CrossoverG1DListPermutations import G1DListCrossoverPMX, G1DListCrossoverOX, \
    G1DListCrossoverOX2, G1DListCrossoverCycle, G1DListCrossoverPOS, G1DListCrossoverMPX, G1DListCrossoverEdge, \
    G1DListCrossoverEPMX, G1DListCrossoverGreedy, G1DListCrossoverIGX, G1DListCrossoverSequentialConstructive


tsp_file_list_all = "a280" ,"att48" ,"att532" ,"bayg29" ,"berlin52" ,"br17" ,"dantzig42" ,"eil51" ,"eil76" ,"eil101" ,"fri26" ,"ft53" ,"ft70" ,"ftv33" ,"ftv35" ,"ftv38" ,"ftv44" ,"ftv47" ,"ftv55" ,"ftv64" ,"ftv70" ,"ftv170" ,"gr17" ,"gr21" ,"gr24" ,"gr666" ,"kro124p" ,"lin105" ,"p43" ,"pcb442" ,"pr76" ,"pr226" ,"rbg323" ,"rbg358" ,"rbg403" ,"rbg443" ,"ry48p" ,"st70" ,"xray14012_1" ,"xray14012_2"
tsp_file_list_euclid_2d= "a280" ,"berlin52" ,"eil101" ,"eil51" ,"eil76" ,"lin105" ,"pcb442" ,"pr226" ,"pr76" ,"st70"

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

crossover_methods = ["GX", "IGX","PMX", "CX", "OX", "OX2", "MPX", "POS", "ERX", "EPMX", "SCX"]



PIL_SUPPORT = None
LAST_SCORE = -1



try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_SUPPORT = True
except ImportError:
    PIL_SUPPORT = False



def get_distance_matrixes(coords):
    """ returns distance matrix as both dict and list """
    matrix_dict = {}
    matrix_list = []
    for i, (x1, y1) in enumerate(coords):
        matrix_list.append([])
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            distance_value = math.sqrt(dx * dx + dy * dy)
            matrix_dict[i, j] = distance_value
            matrix_list[i].insert(j,distance_value)
    return matrix_dict, matrix_list



def tour_length_xy(distance_matrix, tour, cities):
    """ Returns the total length of the tour """
    total = 0
    t = tour.getInternalList()
    for i in range(cities):
        j = (i + 1) % cities
        total += distance_matrix[t[i], t[j]]
    return total


def write_tour_to_img(coords, tour, image_file, max_generation_count):
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
    img.save(image_file, "PNG")
    print(f"The plot was saved into the {image_file} file. max generation: {max_generation_count}")

# This is to make a video of best individuals along the evolution
# see create_video_from_images.bash for example ffmpeg commands.

def evolve_callback_xy(ga_engine):
    global LAST_SCORE
    max_generation_count = ga_engine.getGenerations()
    current_generation = ga_engine.getCurrentGeneration()

    results_directory = ga_engine.getParam("results_directory")
    if results_directory is None:
        raise ValueError("results_directory parameter is not set in the GA engine parameters")  
    
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    coordinates = ga_engine.getParam("coordinates")
    if coordinates is None:
        raise ValueError("coordinates parameter is not set in the GA engine parameters")

    experiment_name = ga_engine.getParam("experiment_name")
    if experiment_name is None:
        raise ValueError("experiment_name parameter is not set in the GA engine parameters")

    if current_generation % 100 == 0:
        best = ga_engine.bestIndividual()
        if LAST_SCORE != best.getRawScore():
            image_filename_digit_count = int(math.floor(math.log10(max_generation_count))) +1
            image_filename = f"{results_directory}/tsp_result_{experiment_name}_{current_generation:0{image_filename_digit_count}}.png"
            write_tour_to_img(coordinates, best, image_filename,max_generation_count)
            LAST_SCORE = best.getRawScore()
    return False

def get_coordinates_for_tsp_problem(problem_name):
    filename = 'tsp_datasets/' + problem_name + '.tsp'
    path = os.path.join(os.path.dirname(__file__), filename)
    problem = tsplib95.load(path)

    coordinates = None
    if problem.edge_weight_type == "EUC_2D":
        coordinates = [tuple(problem.node_coords[i]) for i in range(1, len(list(problem.get_nodes())) + 1)]
        return coordinates
    
    raise ValueError(f"TSP Problem type is not supported, edge_weight_type: {problem.edge_weight_type}" )

def get_coordinates_for_random_cities(
      cities_count=100    
    , cities_random_width=1024 
    , cities_random_height=768
    , random_seed = 1024
    ):
    random.seed(random_seed)    
    coordinates = [(random.randint(0, cities_random_width), random.randint(0, cities_random_height))
              for i in range(cities_count)]
    return coordinates

import inspect

def run_tsp(problem_name:str
             , random_cities_info: dict = None
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

    # 1. Capture the local variables immediately
    current_locals = locals().copy()

    # 2. Get the signature of the function
    sig = inspect.signature(run_tsp)
    
    # 3. Bind using the clean snapshot of locals
    bound_args = sig.bind_partial(**current_locals).arguments

    experiment_name = ""

    print("--- Non-Default run_tsp Function Arguments ---")
    for key, value in bound_args.items():
        default_value = sig.parameters[key].default
        
        if default_value is not inspect.Parameter.empty and value == default_value:
            continue
            
        if value is not None:
            experiment_name += f"{key},{value!r};"
    
    print(experiment_name)

    if "random" in problem_name.lower():
        if random_cities_info is not None:
            coordinates = get_coordinates_for_random_cities(**random_cities_info)
        else:
            coordinates = get_coordinates_for_random_cities()
            experiment_name = problem_name

    if problem_name in tsp_file_list_euclid_2d:
        coordinates = get_coordinates_for_tsp_problem(problem_name)


    cities_count = len(coordinates)
    random.seed(random_seed)
    distance_matrix_dict, distance_matrix_list = get_distance_matrixes(coordinates)
    genome = G1DList.G1DList(len(coordinates))

    genome.setParams(distance_matrix_dict=distance_matrix_dict, distance_matrix_list=distance_matrix_list)
    genome.evaluator.set(lambda chromosome: tour_length_xy(distance_matrix_dict, chromosome, cities_count))
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
    ga.setParams(experiment_name=experiment_name)

    if PIL_SUPPORT:
        ga.stepCallback.set(  evolve_callback_xy)


    start = time.time()
    ga.evolve(freq_stats=10)
    end = time.time()
    best = ga.bestIndividual()
    print(end - start)

    best = ga.bestIndividual()
    #f.write(str(end - start) + "\n")


    if PIL_SUPPORT:
        img_filename = f"{results_directory}/tsp_result_{experiment_name}.png"
        write_tour_to_img(coordinates, best, img_filename,max_generation_count)
    else:
        print("No PIL detected, cannot plot the graph !")
