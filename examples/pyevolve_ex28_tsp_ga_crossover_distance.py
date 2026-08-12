from helper_tsp import run_tsp, crossover_methods




if __name__ == "__main__":
    for co_name in crossover_methods:
        for random_seed in range(1000, 1031):
            run_tsp(problem_name="gr21"
                    , crossover_method=co_name
                    , random_seed=random_seed
                    )