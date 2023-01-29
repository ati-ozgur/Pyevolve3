from .. import Util
from random import randint as rand_randint, gauss as rand_gauss, uniform as rand_uniform
from random import choice as rand_choice
from ..representations.G1DList import G1DList
import numpy as np

from .MutatorG1DList import G1DListMutatorSwap


def G1DListMutatorSwap(genome: G1DList, **args):
    """ The mutator of G1DList, Swap Mutator

    .. note:: this mutator is :term:`Data Type Independent`

    """
    
    mutations = 0
    pmut = args["pmut"]
    if pmut <= 0.0:
        return mutations
    if not Util.randomFlipCoin(pmut):
        return mutations

    listSize = len(genome)
    
    
    to_remove = rand_randint(0, listSize - 1)
    while True:
        to_insert = rand_randint(0, listSize - 1)
        if to_remove != to_insert:
            break

    Util.listSwapElement(genome.genomeList, to_insert, to_remove)
    mutations = mutations + 1

    return mutations

def G1DListMutatorSimpleInversion(genome, **args):
    """ The mutator of G1DList, Simple Inversion Mutation

    .. note:: this mutator is :term:`Data Type Independent`

    """

    mutations = 0
    if args["pmut"] <= 0.0:
        return 0

    cuts = [rand_randint(0, len(genome)), rand_randint(0, len(genome))]

    if cuts[0] > cuts[1]:
        Util.listSwapElement(cuts, 0, 1)

    if (cuts[1] - cuts[0]) <= 0:
        cuts[1] = rand_randint(cuts[0], len(genome))

    if Util.randomFlipCoin(args["pmut"]):
        part = genome[cuts[0]:cuts[1]]
        if len(part) == 0:
            return 0
        part.reverse()
        genome[cuts[0]:cuts[1]] = part
        mutations += 1

    return mutations


def G1DListMutatorScramble(genome, **args):
    """ The mutator of G1DList, Scramble Mutation

    .. note:: this mutator is :term:`Data Type Independent`

    """

    mutations = 0
    if args["pmut"] <= 0.0:
        return 0

    cuts = [rand_randint(0, len(genome)), rand_randint(0, len(genome))]

    if cuts[0] > cuts[1]:
        Util.listSwapElement(cuts, 0, 1)

    if (cuts[1] - cuts[0]) <= 0:
        cuts[1] = rand_randint(cuts[0], len(genome))

    if Util.randomFlipCoin(args["pmut"]):
        part = genome[cuts[0]:cuts[1]]
        if len(part) == 0:
            return 0
        np.random.shuffle(part)
        genome[cuts[0]:cuts[1]] = part
        mutations += 1

    return mutations


def G1DListMutatorDisplacement(genome, **args):
    """ The mutator of G1DList, Displacement Mutation

    .. note:: this mutator is :term:`Data Type Independent`

    """

    mutations = 0
    if args["pmut"] <= 0.0:
        return 0

    cuts = [rand_randint(0, len(genome)), rand_randint(0, len(genome))]

    if cuts[0] > cuts[1]:
        Util.listSwapElement(cuts, 0, 1)

    if (cuts[1] - cuts[0]) <= 0:
        cuts[1] = rand_randint(cuts[0], len(genome))

    if Util.randomFlipCoin(args["pmut"]):
        part = genome[cuts[0]:cuts[1]]
        if len(part) == 0:
            return 0
    del genome.genomeList[cuts[0]:cuts[1]]

    cut = [rand_randint(0, len(genome))]
    for i in range(0, len(part)):
        genome.genomeList.insert(cut[0]+i,part[i])
    mutations += 1

    return mutations

def G1DListMutatorInversion(genome, **args):
    """ The mutator of G1DList, Inversion Mutation

    .. note:: this mutator is :term:`Data Type Independent`

    """

    mutations = 0
    if args["pmut"] <= 0.0:
        return 0

    cuts = [rand_randint(0, len(genome)), rand_randint(0, len(genome))]

    if cuts[0] > cuts[1]:
        Util.listSwapElement(cuts, 0, 1)

    if (cuts[1] - cuts[0]) <= 0:
        cuts[1] = rand_randint(cuts[0], len(genome))

    if Util.randomFlipCoin(args["pmut"]):
        part = genome[cuts[0]:cuts[1]]
        if len(part) == 0:
            return 0
    del genome.genomeList[cuts[0]:cuts[1]]

    cut = [rand_randint(0, len(genome))]
    part.reverse()
    for i in range(0, len(part)):
        genome.genomeList.insert(cut[0]+i,part[i])
    mutations += 1

    return mutations

def G1DListMutatorInsertion(genome, **args):
    """ The mutator of G1DList, Insertion Mutation

    .. note:: this mutator is :term:`Data Type Independent`

    """
    mutations = 0
    pmut = args["pmut"]
    if pmut <= 0.0:
        return mutations
    if not Util.randomFlipCoin(pmut):
        return mutations

    listSize = len(genome)

    to_remove = rand_randint(0, listSize - 1)
    while True:
        to_insert = rand_randint(0, listSize - 1)
        if to_remove != to_insert:
            break

    val = genome.genomeList.pop(to_remove)
    genome.genomeList.insert(to_insert, val)
    mutations = mutations + 1

    return mutations

