import math
import os

PIL_SUPPORT = None
LAST_SCORE = -1



try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_SUPPORT = True
except ImportError:
    PIL_SUPPORT = False


def cartesian_matrix(coords):
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

