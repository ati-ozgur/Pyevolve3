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

