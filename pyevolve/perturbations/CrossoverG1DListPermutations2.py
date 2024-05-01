from random import randint as rand_randint

from pyevolve.perturbations.G1DListCrossoverSRX_Helper import connect_sub_tours, generate_genome

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

    """
    Preliminary experiments revealed that the appropriate length of sub-tours 
    is around sqrt(N), where N is the number of cities.
    """
    g_mom, sister_genome_list = kwargs["mom"], []
    g_dad, brother_genome_list = kwargs["dad"], []
    g_mom_genome_list, g_dad_genome_list = g_mom.genomeList[:], g_dad.genomeList[:]

    genome_length = len(g_mom)
    sub_tour_length = int(genome_length ** 0.5)

    sister, brother = g_mom.clone(), g_dad.clone()
    sister.resetStats()
    brother.resetStats()

    if kwargs["count"] >= 1:
        sister_genome_list = generate_genome(sister_genome_list, g_mom_genome_list, g_dad_genome_list, sub_tour_length)
        sister_genome_list = connect_sub_tours(sister_genome_list)

    if kwargs["count"] == 2:
        brother_genome_list = generate_genome(sister_genome_list, g_mom_genome_list, g_dad_genome_list, sub_tour_length)
        brother_genome_list = connect_sub_tours(brother_genome_list) if kwargs["count"] == 2 else g_dad.genomeList

    sister.genomeList = sister_genome_list
    brother.genomeList = brother_genome_list

    return sister, brother


def G1DListCrossoverCSOX(genome, **kwargs):
    g_mom, g_dad = kwargs["mom"], kwargs["dad"]
    O = [None] * 6
    g_mom_len = len(g_mom)

    r1, r2 = rand_randint(1, g_mom_len - 2), rand_randint(1, g_mom_len - 2)

    for i in range(3):
        if i == 0:
            pos1, pos2 = r1, r2

            p1 = [c for c in g_mom[pos2 + 1:] + g_mom[:pos2 + 1] if c not in g_dad[pos1:pos2 + 1]]
            p2 = [c for c in g_dad[pos2 + 1:] + g_dad[:pos2 + 1] if c not in g_mom[pos1:pos2 + 1]]
        elif i == 1:
            pos1, pos2 = 0, r1 - 1

            p1 = [c for c in g_mom[pos2 + 1:] + g_mom[:pos2 + 1] if c not in g_dad[pos1:pos2 + 1]]
            p2 = [c for c in g_dad[pos2 + 1:] + g_dad[:pos2 + 1] if c not in g_mom[pos1:pos2 + 1]]
        elif i == 2:
            pos1, pos2 = r2 + 1, g_mom_len - 1

            p1 = [c for c in g_mom if c not in g_dad[pos1:pos2 + 1]]
            p2 = [c for c in g_dad if c not in g_mom[pos1:pos2 + 1]]

        O[2 * i], O[2 * i + 1] = [None] * g_mom_len, [None] * g_mom_len

        O[2 * i] = p2[-pos1:] + g_mom[pos1:pos2 + 1] + p2[:g_mom_len - 1 - pos2]
        O[2 * i + 1] = p1[-pos1:] + g_dad[pos1:pos2 + 1] + p1[:g_mom_len - 1 - pos2]
