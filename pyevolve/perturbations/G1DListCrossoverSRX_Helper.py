from random import randint as rand_randint
from typing import List


def connect_sub_tours(sub_tours: List[list]) -> list:
    """
    (0, 0):
        if the closest values are at the head of the queue,
        reverse the second and add the first

    (0, -1):
        if the closest values are at the head of the first, and the tail of the second
        takes the second one and adds the first one

    (-1, 0):
        if the closest values are at the tail of the first and the head of the second
        takes the first one and adds the second one

    (-1, -1):
        if the closest values are at the tail of the queue,
        take the first one and add the reversed second one
    """

    operations = {
        (0, 0): lambda x, y: y[::-1] + x,
        (0, -1): lambda x, y: y + x,
        (-1, 0): lambda x, y: x + y,
        (-1, -1): lambda x, y: x + y[::-1]
    }

    connected_sub_tour = sub_tours.pop(0)

    while sub_tours:
        nearest_sub_tour, nearest_index, nearest_edge = find_nearest_sub_tour(connected_sub_tour, sub_tours)
        operation = operations.get(nearest_edge)

        if operation:
            connected_sub_tour = operation(connected_sub_tour, nearest_sub_tour)
        sub_tours.pop(nearest_index)

    return connected_sub_tour


def find_nearest_sub_tour(sub_tour: list, sub_tours: List[list]) -> (list, int):
    min_diff = float('inf')
    nearest_sub_tour, nearest_index, nearest_edges = None, None, None

    for index, current_sub_tour in enumerate(sub_tours):
        diffs = [
            (abs(sub_tour[0] - current_sub_tour[0]), (0, 0)),
            (abs(sub_tour[0] - current_sub_tour[-1]), (0, -1)),
            (abs(sub_tour[-1] - current_sub_tour[0]), (-1, 0)),
            (abs(sub_tour[-1] - current_sub_tour[-1]), (-1, -1))
        ]

        for diff, edges in diffs:
            if diff < min_diff:
                min_diff = diff
                nearest_sub_tour = current_sub_tour
                nearest_index = index
                nearest_edges = edges

    return nearest_sub_tour, nearest_index, nearest_edges


def generate_genome(child: list, g_mom_genome_list: list, g_dad_genome_list: list, sub_tour_length: int) -> list:
    genome_set = set()

    while g_mom_genome_list or g_dad_genome_list:
        city_index = rand_randint(0, len(g_mom_genome_list) - 1)
        sub_tour = []

        while len(sub_tour) < sub_tour_length and city_index < len(g_mom_genome_list):
            city = g_mom_genome_list[city_index]

            if city not in genome_set:
                genome_set.add(city)
                sub_tour.append(city)
                g_dad_genome_list.remove(city)
                g_mom_genome_list.remove(city)

            city_index += 1

        if sub_tour:
            child.append(sub_tour)

        city_index = rand_randint(0, len(g_dad_genome_list) - 1) if g_dad_genome_list else 0
        sub_tour = []

        while len(sub_tour) < sub_tour_length and city_index < len(g_dad_genome_list):
            city = g_dad_genome_list[city_index]

            if city not in genome_set:
                genome_set.add(city)
                sub_tour.append(city)
                g_mom_genome_list.remove(city)
                g_dad_genome_list.remove(city)

            city_index += 1

        if sub_tour:
            child.append(sub_tour)

    return child
