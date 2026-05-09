


from helper_tsp import run_tsp_random_coordinate_cities, get_coordinates_for_random_cities

if __name__ == "__main__":
    coordinates = get_coordinates_for_random_cities()
    run_tsp_random_coordinate_cities(experiment_name="tsp_default",coordinates=coordinates)
