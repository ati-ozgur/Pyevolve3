import os

import tsplib95

from helper_tsp import crossover_methods, dict_crossoever_operators
from helper_tsp_selector import run_experiment_series, run_selector_ga


GENERATION_COUNT = 1001
STRATEGY = "deterministic"


def main_run(crossover_operator_func, problemname, log_file):
    dataset = os.path.join(os.path.dirname(__file__), "tsp_datasets", problemname + ".tsp")
    problem = tsplib95.load(dataset)
    city_count = len(list(problem.get_nodes()))
    distance_matrix = {
        (i, j): problem.get_weight(i, j)
        for i in range(city_count)
        for j in range(city_count)
    }
    run_selector_ga(
        crossover_operator_func,
        distance_matrix,
        city_count,
        log_file,
        STRATEGY,
        generation_count=GENERATION_COUNT,
    )


if __name__ == "__main__":
    run_experiment_series(main_run, crossover_methods, dict_crossoever_operators, "br17", STRATEGY)
