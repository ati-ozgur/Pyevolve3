


from helper_tsp import run_tsp_random_coordinate_cities, get_random_coordinate_cities

if __name__ == "__main__":
    coordinates = get_random_coordinate_cities()
    run_tsp_random_coordinate_cities(experiment_name="tsp_default",coordinates=coordinates)
