"""Capacitated vehicle routing (CVRP) helpers built on the bundled CVRP instances."""

from dataclasses import dataclass

from pyevolve.planning.datasets import load_vrp_problem


@dataclass
class CVRPInstance:
    """A CVRP instance with nodes re-indexed to ``0..node_count-1`` (depot is ``depot_index``)."""

    node_count: int
    depot_index: int
    capacity: int
    demands: dict
    customers: list
    distance_matrix_dict: dict
    distance_matrix_list: list


def load_cvrp_instance(problem_name, size="small"):
    """Load a bundled CVRP instance (e.g. ``"A-n33-k5"``) and build its distance matrices and demands."""
    problem = load_vrp_problem(problem_name, size)
    original_nodes = list(problem.get_nodes())
    # Put the depot first so it becomes index 0
    depot_node = problem.depots[0] if problem.depots else original_nodes[0]
    original_nodes.remove(depot_node)
    original_nodes.insert(0, depot_node)
    node_count = len(original_nodes)
    node_indexes = {node: index for index, node in enumerate(original_nodes)}
    depot_index = 0

    distance_matrix_dict = {
        (row, column): float(problem.get_weight(original_nodes[row], original_nodes[column]))
        for row in range(node_count)
        for column in range(node_count)
    }
    distance_matrix_list = [
        [distance_matrix_dict[row, column] for column in range(node_count)]
        for row in range(node_count)
    ]
    demands = {node_indexes[node]: problem.demands.get(node, 0) for node in original_nodes}
    customers = [node for node in range(node_count) if node != depot_index]

    return CVRPInstance(
        node_count=node_count,
        depot_index=depot_index,
        capacity=problem.capacity,
        demands=demands,
        customers=customers,
        distance_matrix_dict=distance_matrix_dict,
        distance_matrix_list=distance_matrix_list,
    )


def make_cvrp_fitness(instance):
    """Return an evaluator for a giant-tour chromosome of customers.

    The route returns to the depot whenever the next customer would exceed the vehicle capacity.
    """
    distances = instance.distance_matrix_dict
    depot = instance.depot_index

    def cvrp_fitness(chromosome):
        total_distance = 0.0
        current_load = 0
        last_node = depot

        for node in chromosome.getInternalList():
            demand = instance.demands.get(node, 0)
            if current_load + demand > instance.capacity:
                total_distance += distances[last_node, depot]
                total_distance += distances[depot, node]
                current_load = demand
            else:
                total_distance += distances[last_node, node]
                current_load += demand
            last_node = node

        return total_distance + distances[last_node, depot]

    return cvrp_fitness
