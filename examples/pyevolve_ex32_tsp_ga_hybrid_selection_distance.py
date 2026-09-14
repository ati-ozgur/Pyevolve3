import os
import tsplib95
import numpy

from helper_tsp import crossover_methods, dict_crossoever_operators
from helper_tsp import get_distance_matrixes_from_tsp_problem
from helper_tsp_selector import run_experiment_series, run_selector_ga


GENERATION_COUNT = 1001
STRATEGY = "deterministic"


def main_run(crossover_operator_func, problemname, log_file):
 
    distance_matrix, distance_matrix_list = get_distance_matrixes_from_tsp_problem(problemname)
    cities_count = len(distance_matrix_list)

    run_selector_ga(
        crossover_operator_func,
        distance_matrix,
        cities_count,
        log_file,
        STRATEGY,
        generation_count=GENERATION_COUNT,
    )


if __name__ == "__main__":
    dataset_name = "br17"
    # dataset_name = "random_data_30_order_transitions_CSP"
    run_experiment_series(
        main_run,
        crossover_methods,
        dict_crossoever_operators,
        dataset_name,
        STRATEGY,
        include_strategy_in_filename=False,
    )
