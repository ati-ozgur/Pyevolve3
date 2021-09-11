"""

:mod:`Crossovers` -- crossover methods module
=====================================================================

In this module we have the genetic operators of crossover (or recombination) for each chromosome representation.

"""


from random import randint as rand_randint, choice as rand_choice
from random import random as rand_random
import math
from .. import Util


# 1D Binary String

def G1DBinaryStringXSinglePoint(genome, **args):
    """ The crossover of 1D Binary String, Single Point

    .. warning:: You can't use this crossover method for binary strings with length of 1.

    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    if len(gMom) == 1:
        Util.raiseException(
            "The Binary String have one element, can't use the Single Point Crossover method !", TypeError)

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


def G1DBinaryStringXTwoPoint(genome, **args):
    """ The 1D Binary String crossover, Two Point

    .. warning:: You can't use this crossover method for binary strings with length of 1.

    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    if len(gMom) == 1:
        Util.raiseException("The Binary String have one element, can't use the Two Point Crossover method !", TypeError)

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


def G1DBinaryStringXUniform(genome, **args):
    """ The G1DList Uniform Crossover """
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
        if Util.randomFlipCoin(Consts.CDefG1DBinaryStringUniformProb):
            temp = sister[i]
            sister[i] = brother[i]
            brother[i] = temp

    return (sister, brother)


#  2D Binary String

def G2DBinaryStringXUniform(genome, **args):
    """ The G2DBinaryString Uniform Crossover

    .. versionadded:: 0.6
       The *G2DBinaryStringXUniform* function
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

    h, w = gMom.getSize()

    for i in range(h):
        for j in range(w):
            if Util.randomFlipCoin(Consts.CDefG2DBinaryStringUniformProb):
                temp = sister.getItem(i, j)
                sister.setItem(i, j, brother.getItem(i, j))
                brother.setItem(i, j, temp)

    return (sister, brother)


def G2DBinaryStringXSingleVPoint(genome, **args):
    """ The crossover of G2DBinaryString, Single Vertical Point

    .. versionadded:: 0.6
       The *G2DBinaryStringXSingleVPoint* function
    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    cut = rand_randint(1, gMom.getWidth() - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        for i in range(sister.getHeight()):
            sister[i][cut:] = gDad[i][cut:]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        for i in range(brother.getHeight()):
            brother[i][cut:] = gMom[i][cut:]

    return (sister, brother)


def G2DBinaryStringXSingleHPoint(genome, **args):
    """ The crossover of G2DBinaryString, Single Horizontal Point

    .. versionadded:: 0.6
       The *G2DBinaryStringXSingleHPoint* function

    """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    cut = rand_randint(1, gMom.getHeight() - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        for i in range(cut, sister.getHeight()):
            sister[i][:] = gDad[i][:]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        for i in range(brother.getHeight()):
            brother[i][:] = gMom[i][:]

    return (sister, brother)

