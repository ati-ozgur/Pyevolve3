from random import randint as rand_randint


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
