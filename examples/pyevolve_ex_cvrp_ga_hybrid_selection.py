from pyevolve.planning import dict_crossoever_operators, load_cvrp_instance, make_cvrp_fitness
from pyevolve.planning.selector_helper import run_experiment_series, run_selector_ga


GENERATION_COUNT = 3
STRATEGY = "deterministic"
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
    instance = load_cvrp_instance(problemname, size="small")

    run_selector_ga(
        crossover_func,
        instance.distance_matrix_dict,
        instance.node_count,
        log_file,
        STRATEGY,
        generation_count=GENERATION_COUNT,
        evaluator=make_cvrp_fitness(instance),
        genome_values=instance.customers,
        distance_matrix_list=instance.distance_matrix_list,
    )


if __name__ == "__main__":
    run_experiment_series(
        main_run,
        CVRP_CROSSOVER_METHODS,
        dict_crossoever_operators,
        "A-n33-k5",
        STRATEGY,
    )
