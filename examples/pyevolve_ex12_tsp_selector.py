from helper_tsp import run_tsp_random_coordinate_cities,get_coordinates_for_random_cities
from pyevolve.selections import SelectionRank


if __name__ == "__main__":
    coordinates = get_coordinates_for_random_cities()
    run_tsp_random_coordinate_cities(experiment_name="tsp_selector"
        , coordinates=coordinates
        , selection_method=SelectionRank.SelectorLinearRanking)
