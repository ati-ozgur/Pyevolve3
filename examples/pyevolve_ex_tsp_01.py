


from helper_tsp import run_tsp

if __name__ == "__main__":
    #run_tsp(problem_name="tsp_random_cities_default"
    #        , crossover_method="SNGL"
    #        , freq_stats=1
    #        )
    run_tsp(problem_name="gr21"
            , crossover_method="SNGL"
            , freq_stats=1
            )