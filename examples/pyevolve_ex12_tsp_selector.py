from helper_tsp import run_tsp
from pyevolve.selections import SelectionRank


if __name__ == "__main__":


    run_tsp(experiment_name="tsp_selector",
        selection_method=SelectionRank.SelectorLinearRanking)
