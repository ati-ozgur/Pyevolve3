from random import randint as rand_randint, choice as rand_choice
from random import random as rand_random
import math
from .. import Util



# 1D List

def G1DListCrossoverSinglePoint(genome, **args):
    """ The crossover of G1DList, Single Point

    .. warning:: You can't use this crossover method for lists with just one element.

    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    if len(gMom) == 1:
        Util.raiseException("The 1D List have one element, can't use the Single Point Crossover method !", TypeError)

    cut = rand_randint(1, len(gMom) - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister[cut:] = gDad[cut:]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother[cut:] = gMom[cut:]

    return (sister, brother)


def G1DListCrossoverTwoPoint(genome, **args):
    """ The G1DList crossover, Two Point

    .. warning:: You can't use this crossover method for lists with just one element.

    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    if len(gMom) == 1:
        Util.raiseException("The 1D List have one element, can't use the Two Point Crossover method !", TypeError)

    cuts = [rand_randint(1, len(gMom) - 1), rand_randint(1, len(gMom) - 1)]

    if cuts[0] > cuts[1]:
        Util.listSwapElement(cuts, 0, 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister[cuts[0]:cuts[1]] = gDad[cuts[0]:cuts[1]]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother[cuts[0]:cuts[1]] = gMom[cuts[0]:cuts[1]]

    return (sister, brother)


def G1DListCrossoverUniform(genome, **args):
    """ The G1DList Uniform Crossover

    Each gene has a 50% chance of being swapped between mom and dad

    """
    from . import Consts
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    sister = gMom.clone()
    brother = gDad.clone()
    sister.resetStats()
    brother.resetStats()

    for i in range(len(gMom)):
        if Util.randomFlipCoin(Consts.CDefG1DListCrossUniformProb):
            temp = sister[i]
            sister[i] = brother[i]
            brother[i] = temp

    return (sister, brother)


def G1DListCrossoverOX(genome, **args):
    """ The OX Crossover for G1DList  (order crossover) """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)

    c1, c2 = [rand_randint(1, len(gMom) - 1), rand_randint(1, len(gMom) - 1)]

    while c1 == c2:
        c2 = rand_randint(1, len(gMom) - 1)

    if c1 > c2:
        h = c1
        c1 = c2
        c2 = h

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        P1 = [c for c in gMom[c2:] + gMom[:c2] if c not in gDad[c1:c2]]
        sister.genomeList = P1[listSize - c2:] + gDad[c1:c2] + P1[:listSize - c2]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        P2 = [c for c in gDad[c2:] + gDad[:c2] if c not in gMom[c1:c2]]
        brother.genomeList = P2[listSize - c2:] + gMom[c1:c2] + P2[:listSize - c2]

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)


def G1DListCrossoverEdge(genome, **args):
    """ The Edge Recombination crossover for G1DList (widely used for TSP problem)

    See more information in the `Edge Recombination Operator
    <http://en.wikipedia.org/wiki/Edge_recombination_operator>`_
    Wikipedia entry.
    """
    gMom, sisterl = args["mom"], []
    gDad, brotherl = args["dad"], []

    mom_edges, dad_edges, merge_edges = Util.G1DListGetEdgesComposite(gMom, gDad)

    for c, u in (sisterl, set(gMom)), (brotherl, set(gDad)):
        curr = None
        for i in range(len(gMom)):
            curr = rand_choice(tuple(u)) if not curr else curr
            c.append(curr)
            u.remove(curr)
            d = [v for v in merge_edges.get(curr, []) if v in u]
            if d:
                curr = rand_choice(d)
            else:
                s = [v for v in mom_edges.get(curr, []) if v in u]
                s += [v for v in dad_edges.get(curr, []) if v in u]
                curr = rand_choice(s) if s else None

    sister = gMom.clone()
    brother = gDad.clone()
    sister.resetStats()
    brother.resetStats()

    sister.genomeList = sisterl
    brother.genomeList = brotherl

    return (sister, brother)




def G1DListCrossoverCutCrossfill(genome, **args):
    """ The crossover of G1DList, Cut and crossfill, for permutations
    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    if len(gMom) == 1:
        Util.raiseException("The 1D List have one element, can't use the Single Point Crossover method !", TypeError)

    cut = rand_randint(1, len(gMom) - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        mother_part = gMom[0:cut]
        sister.resetStats()
        i = (len(sister) - cut)
        x = 0
        for v in gDad:
            if v in mother_part:
                continue
            if x >= i:
                break
            sister[cut + x] = v
            x += 1

    if args["count"] == 2:
        brother = gDad.clone()
        father_part = gDad[0:cut]
        brother.resetStats()
        i = (len(brother) - cut)
        x = 0
        for v in gMom:
            if v in father_part:
                continue
            if x >= i:
                break
            brother[cut + x] = v
            x += 1

    return (sister, brother)


def G1DListCrossoverRealSBX(genome, **args):
    """ Experimental SBX Implementation - Follows the implementation in NSGA-II (Deb, et.al)

    Some implementation `reference <http://vision.ucsd.edu/~sagarwal/icannga.pdf>`_.
    And another reference to the `Simulated Binary Crossover
    <http://www.mitpressjournals.org/doi/abs/10.1162/106365601750190406>`_.

    .. warning:: This crossover method is Data Type Dependent, which means that
                 must be used for 1D genome of real values.
    """
    from . import Consts

    EPS = Consts.CDefG1DListSBXEPS
    # Crossover distribution index
    eta_c = Consts.CDefG1DListSBXEtac

    gMom = args["mom"]
    gDad = args["dad"]

    # Get the variable bounds ('gDad' could have been used; but I love Mom:-))
    lb = gMom.getParam("rangemin", Consts.CDefRangeMin)
    ub = gMom.getParam("rangemax", Consts.CDefRangeMax)

    sister = gMom.clone()
    brother = gDad.clone()

    sister.resetStats()
    brother.resetStats()

    for i in range(0, len(gMom)):
        if math.fabs(gMom[i] - gDad[i]) > EPS:
            if gMom[i] > gDad[i]:
                # swap
                temp = gMom[i]
                gMom[i] = gDad[i]
                gDad[i] = temp

            # random number betwn. 0 & 1
            u = rand_random()

            beta = 1.0 + 2 * (gMom[i] - lb) / (1.0 * (gDad[i] - gMom[i]))
            alpha = 2.0 - beta ** (-(eta_c + 1.0))

            if u <= (1.0 / alpha):
                beta_q = (u * alpha) ** (1.0 / ((eta_c + 1.0) * 1.0))
            else:
                beta_q = (1.0 / (2.0 - u * alpha)) ** (1.0 / (1.0 * (eta_c + 1.0)))

            brother[i] = 0.5 * ((gMom[i] + gDad[i]) - beta_q * (gDad[i] - gMom[i]))

            beta = 1.0 + 2.0 * (ub - gDad[i]) / (1.0 * (gDad[i] - gMom[i]))
            alpha = 2.0 - beta ** (-(eta_c + 1.0))

            if u <= (1.0 / alpha):
                beta_q = (u * alpha) ** (1.0 / ((eta_c + 1) * 1.0))
            else:
                beta_q = (1.0 / (2.0 - u * alpha)) ** (1.0 / (1.0 * (eta_c + 1.0)))

            sister[i] = 0.5 * ((gMom[i] + gDad[i]) + beta_q * (gDad[i] - gMom[i]))

            if brother[i] > ub:
                brother[i] = ub
            if brother[i] < lb:
                brother[i] = lb

            if sister[i] > ub:
                sister[i] = ub
            if sister[i] < lb:
                sister[i] = lb

            if rand_random() > 0.5:
                # Swap
                temp = sister[i]
                sister[i] = brother[i]
                brother[i] = temp
        else:
            sister[i] = gMom[i]
            brother[i] = gDad[i]

    return (sister, brother)

