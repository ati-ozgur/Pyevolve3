import os

import tsplib95

from helper_tsp import crossover_methods, dict_crossoever_operators, get_distance_matrixes_from_coordinates
from helper_tsp_selector import run_experiment_series, run_selector_ga


GENERATION_COUNT = 1001
STRATEGY = "deterministic"


def main_run(crossover_operator_func, problemname, log_file):
    path = os.path.join(os.path.dirname(__file__), "tsp_datasets", problemname + ".tsp")
    problem = tsplib95.load(path)
    coordinates = [tuple(problem.node_coords[index]) for index in problem.get_nodes()]
    distance_matrix, _ = get_distance_matrixes_from_coordinates(coordinates)
    run_selector_ga(
        crossover_operator_func,
        distance_matrix,
        len(coordinates),
        log_file,
        STRATEGY,
        generation_count=GENERATION_COUNT,
        coordinates=coordinates,
        save_images=False,
    )


if __name__ == "__main__":
    run_experiment_series(main_run, crossover_methods, dict_crossoever_operators, "eil51", STRATEGY)
