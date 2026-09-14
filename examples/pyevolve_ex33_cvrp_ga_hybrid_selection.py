import os

import tsplib95

from helper_tsp import dict_crossoever_operators
from helper_tsp_selector import run_experiment_series, run_selector_ga


GENERATION_COUNT = 1001
STRATEGY = "deterministic"
PROBLEM_DIRECTORY = os.path.join(os.path.dirname(__file__), "vrp_datasets", "small")
CVRP_CROSSOVER_METHODS = (
    "PMX",
    "CX",
    "OX",
    "OX2",
    "MPX",
    "POS",
    "ERX",
    "EPMX",
    "GX",
    "IGX",
    "SCX",
)


def main_run(crossover_func, problemname, log_file):
    problem_path = os.path.join(PROBLEM_DIRECTORY, problemname + ".vrp")
    problem = tsplib95.load(problem_path)
    original_nodes = list(problem.get_nodes())
    node_count = len(original_nodes)
    node_indexes = {node: index for index, node in enumerate(original_nodes)}
    depot_index = 0
    capacity = problem.capacity

    distance_matrix = {
        (row, column): float(problem.get_weight(original_nodes[row], original_nodes[column]))
        for row in range(node_count)
        for column in range(node_count)
    }
    demands = {
        node_indexes[node]: problem.demands.get(node, 0)
        for node in original_nodes
    }
    customers = [node for node in range(node_count) if node != depot_index]

    def cvrp_fitness(chromosome):
        total_distance = 0.0
        current_load = 0
        last_node = depot_index

        for node in chromosome.getInternalList():
            demand = demands.get(node, 0)
            if current_load + demand > capacity:
                total_distance += distance_matrix[last_node, depot_index]
                total_distance += distance_matrix[depot_index, node]
                current_load = demand
            else:
                total_distance += distance_matrix[last_node, node]
                current_load += demand
            last_node = node

        return total_distance + distance_matrix[last_node, depot_index]

    run_selector_ga(
        crossover_func,
        distance_matrix,
        node_count,
        log_file,
        STRATEGY,
        generation_count=GENERATION_COUNT,
        evaluator=cvrp_fitness,
        genome_values=customers,
    )


if __name__ == "__main__":
    run_experiment_series(
        main_run,
        CVRP_CROSSOVER_METHODS,
        dict_crossoever_operators,
        "A-n33-k5",
        STRATEGY,
    )
