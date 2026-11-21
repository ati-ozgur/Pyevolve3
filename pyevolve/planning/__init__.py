"""Routing/planning problems (TSP, CVRP): bundled datasets and experiment harnesses.

Typical use::

    from pyevolve.planning import run_tsp
    run_tsp("att48", crossover_method="ERX")

Needs the optional dependencies from ``pip install "Pyevolve3[planning]"``.
"""

from pyevolve.planning.datasets import (
    list_tsp_problems,
    list_vrp_problems,
    load_tsp_problem,
    load_vrp_problem,
)
from pyevolve.planning.tsp_helper import (
    crossover_methods,
    dict_crossoever_operators,
    get_coordinates_for_random_cities,
    get_coordinates_for_tsp_problem,
    get_distance_matrixes_from_coordinates,
    get_distance_matrixes_from_tsp_problem,
    get_tsp_problem,
    run_tsp,
    tour_length,
    tsp_file_list_all,
    tsp_file_list_euclid_2d,
    write_tour_to_img,
)
from pyevolve.planning.cvrp import CVRPInstance, load_cvrp_instance, make_cvrp_fitness

__all__ = [
    "CVRPInstance",
    "crossover_methods",
    "dict_crossoever_operators",
    "get_coordinates_for_random_cities",
    "get_coordinates_for_tsp_problem",
    "get_distance_matrixes_from_coordinates",
    "get_distance_matrixes_from_tsp_problem",
    "get_tsp_problem",
    "list_tsp_problems",
    "list_vrp_problems",
    "load_cvrp_instance",
    "load_tsp_problem",
    "load_vrp_problem",
    "make_cvrp_fitness",
    "run_tsp",
    "tour_length",
    "tsp_file_list_all",
    "tsp_file_list_euclid_2d",
    "write_tour_to_img",
]
