from pyevolve.planning import (
    crossover_methods,
    dict_crossoever_operators,
    get_distance_matrixes_from_coordinates,
    load_tsp_problem,
)
from pyevolve.planning.selector_helper import run_experiment_series, run_selector_ga


GENERATION_COUNT = 3
STRATEGY = "deterministic"


def main_run(crossover_operator_func, problemname, log_file):
    problem = load_tsp_problem(problemname)
    coordinates = [tuple(problem.node_coords[index]) for index in problem.get_nodes()]
    distance_matrix, distance_matrix_list = get_distance_matrixes_from_coordinates(
        coordinates
    )
    run_selector_ga(
        crossover_operator_func,
        distance_matrix,
        len(coordinates),
        log_file,
        STRATEGY,
        generation_count=GENERATION_COUNT,
        coordinates=coordinates,
        save_images=False,
        distance_matrix_list=distance_matrix_list,
    )


if __name__ == "__main__":
    run_experiment_series(main_run, crossover_methods, dict_crossoever_operators, "eil51", STRATEGY)
