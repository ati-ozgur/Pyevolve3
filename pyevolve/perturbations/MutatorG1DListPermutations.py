from .. import Util
from random import randint as rand_randint, gauss as rand_gauss, uniform as rand_uniform
from random import choice as rand_choice
from ..representations.G1DList import G1DList


from .MutatorG1DList import G1DListMutatorSwap


def G1DListMutatorDisplacement(genome: G1DList, **args):
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

    val = genome.genomeList.pop(to_remove)
    genome.genomeList.insert(to_insert, val)
    mutations = mutations + 1

    return mutations

