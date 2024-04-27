from random import randint as rand_randint
from typing import List

"""
g_mom.genomeList -> 1D List
g_mom.genomeList = [27, 30, 36, 50, 39, 6, 24, 9, 13, 43, 10, 20, 29, 22, 40, 7, 33, 1, 34, 28, 31, 26, 16, 25, 12, 8, 45, 4, 2, 49, 0, 44, 17, 41, 32, 21, 48, 19, 37, 35, 42, 47, 15, 46, 3, 23, 11, 38, 14, 5, 18]

sister or brother are clones of the parents.
The difference is hidden in their genomeList.

sister = g_mom.clone()
sister.genomeList = [22, 40, 7, 31, 26, 16, 45, 2, 49, 44, 47, 15, 3, 23, 19, 48, 14, 8, 5, 1, 27, 29, 11, 4, 21, 9, 18, 24, 34, 25, 42, 39, 38, 37, 33, 10, 30, 17, 46, 6, 28, 36, 43, 12, 41, 32, 35, 13, 0, 50, 20]
"""


def G1DListCrossoverOX6(genome, **kwargs):
    """ The OX6 Crossover for G1DList  (order crossover)

    See more information in the `Solving travelling salesman problem
    using genetic algorithm based on heuristic crossover and mutation operator
    <https://www.impactjournals.us/index.php/download/archives/--1391174555-4.%20Eng-Solving%20Travelling%20Salesman-Kanchan%20Rani.pdf>'
    """

    sister = None
    brother = None
    g_mom = kwargs["mom"]
    g_dad = kwargs["dad"]
    list_size = len(g_mom)

    c1, c2 = rand_randint(0, list_size - 1), rand_randint(0, list_size - 1)

    while c1 == c2:
        c2 = rand_randint(0, list_size - 1)

    if c1 > c2:
        c1, c2 = c2, c1

    if kwargs["count"] >= 1:
        sister = g_mom.clone()
        sister.resetStats()
        p1 = [c for c in g_dad if c not in g_mom[c1:c2]]
        sister.genomeList = p1[:c1] + g_mom[c1:c2] + p1[c1:]

    if kwargs["count"] == 2:
        brother = g_dad.clone()
        sister.resetStats()
        p1 = [c for c in g_mom if c not in g_dad[c1:c2]]
        brother.gnomeList = p1[:c1] + g_mom[c1:c2] + p1[c1:]

    assert list_size == len(sister)
    assert list_size == len(brother)

    return sister, brother


def G1DListCrossoverHX(genome, **kwargs):
    """ The HX Crossover for G1DList  (half crossover)

    See more information in the `Analysis of the suitability
    of using blind crossover operators in genetic algorithms
    for solving routing problems
    <https://ieeexplore.ieee.org/abstract/document/6608960>'
    """

    sister = None
    brother = None
    g_mom = kwargs["mom"]
    g_dad = kwargs["dad"]
    list_size = len(g_mom)
    half_size = list_size // 2

    if kwargs["count"] >= 1:
        sister = g_mom.clone()
        sister.resetStats()
        p1 = [c for c in g_dad if c not in g_mom[:half_size]]
        sister.genomeList = g_mom[:half_size] + p1

    if kwargs["count"] == 2:
        brother = g_dad.clone()
        brother.resetStats()
        p1 = [c for c in g_mom if c not in g_dad[:half_size]]
        brother.genomeList = g_dad[:half_size] + p1

    assert list_size == len(sister)
    assert list_size == len(brother)

    return sister, brother


# Doesn't respect overlap.
def G1DListCrossoverTPX(genome, **kwargs):
    """ The TPX Crossover for G1DList  (two-point crossover)

    See more information in the
    <https://scholar.google.com/scholar?output=instlink&q=info:7d_ZB2LqT3QJ:scholar.google.com/&hl=tr&as_sdt=0,5&scillfp=480710777611443790&oi=lle>
    <https://scholar.archive.org/work/yxts2ace4rcxfjugvhdjby2o3a/access/wayback/https://www.isr-publications.com/jmcs/691/download-ccgdc-a-new-crossover-operator-for-genetic-data-clustering>
    """

    sister = None
    brother = None
    g_mom = kwargs["mom"]
    g_dad = kwargs["dad"]
    list_size = len(g_mom)

    c1, c2 = rand_randint(0, list_size - 1), rand_randint(0, list_size - 1)

    while c1 == c2:
        c2 = rand_randint(0, list_size - 1)

    if c1 > c2:
        c1, c2 = c2, c1

    if kwargs["count"] >= 1:
        sister = g_mom.clone()
        sister.resetStats()
        p1 = [c for c in g_mom[c1:c2]]
        sister.genomeList = g_dad[:c1] + p1 + g_dad[c2:]

    if kwargs["count"] == 2:
        brother = g_dad.clone()
        brother.resetStats()
        p1 = [c for c in g_dad[c1:c2]]
        sister.genomeList = g_mom[:c1] + p1 + g_mom[c2:]

    assert list_size == len(sister)
    assert list_size == len(brother)

    return sister, brother


def G1DListCrossoverSRX(genome, **kwargs):
    """
    Sub-tour Recombination crossover for TSP

    <https://link.springer.com/article/10.1007/s10015-010-0866-8>
    """

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
        nearest_sub_tour = None
        nearest_index = None
        nearest_edges = None

        for i, current_sub_tour in enumerate(sub_tours):
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
                    nearest_index = i
                    nearest_edges = edges

        return nearest_sub_tour, nearest_index, nearest_edges

    def generate_genome(child: list) -> list:
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

    """
    Preliminary experiments revealed that the appropriate length of sub-tours 
    is around sqrt(N), where N is the number of cities.
    """
    g_mom, sister_genome_list = kwargs["mom"], []
    g_dad, brother_genome_list = kwargs["dad"], []
    genome_length = len(g_mom)
    sub_tour_length = int(genome_length ** 0.5)

    sister = g_mom.clone()
    brother = g_dad.clone()
    brother.resetStats()
    sister.resetStats()

    g_mom_genome_list = g_mom.genomeList[:]
    g_dad_genome_list = g_dad.genomeList[:]

    if kwargs["count"] >= 1:
        sister_genome_list = generate_genome(sister_genome_list)
        sister_genome_list = connect_sub_tours(sister_genome_list)

        g_mom_genome_list = g_mom.genomeList[:]
        g_dad_genome_list = g_dad.genomeList[:]

    if kwargs["count"] == 2:
        brother_genome_list = generate_genome(brother_genome_list)
        brother_genome_list = connect_sub_tours(brother_genome_list) if kwargs["count"] == 2 else g_dad.genomeList

    sister.genomeList = sister_genome_list
    brother.genomeList = brother_genome_list

    return sister, brother
