from helper_tsp import run_tsp
from pyevolve.selections import SelectionRank


if __name__ == "__main__":
    run_tsp(problem_name="tsp_random_cities_SelectorLinearRanking"
        , selection_method=SelectionRank.SelectorLinearRanking)
