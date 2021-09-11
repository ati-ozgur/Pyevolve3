from .. import Util
from random import randint as rand_randint, gauss as rand_gauss, uniform as rand_uniform
from random import choice as rand_choice


# 1D Binary String

def G1DBinaryStringMutatorSwap(genome, **args):
    """ The 1D Binary String Swap Mutator """

    if args["pmut"] <= 0.0:
        return 0
    stringLength = len(genome)
    mutations = args["pmut"] * (stringLength)

    if mutations < 1.0:
        mutations = 0
        for it in range(stringLength):
            if Util.randomFlipCoin(args["pmut"]):
                Util.listSwapElement(genome, it, rand_randint(0, stringLength - 1))
                mutations += 1

    else:
        for it in range(int(round(mutations))):
            Util.listSwapElement(genome, rand_randint(0, stringLength - 1),
                                 rand_randint(0, stringLength - 1))

    return int(mutations)


def G1DBinaryStringMutatorFlip(genome, **args):
    """ The classical flip mutator for binary strings """
    if args["pmut"] <= 0.0:
        return 0
    stringLength = len(genome)
    mutations = args["pmut"] * (stringLength)

    if mutations < 1.0:
        mutations = 0
        for it in range(stringLength):
            if Util.randomFlipCoin(args["pmut"]):
                if genome[it] == 0:
                    genome[it] = 1
                else:
                    genome[it] = 0
                mutations += 1

    else:
        for it in range(int(round(mutations))):
            which = rand_randint(0, stringLength - 1)
            if genome[which] == 0:
                genome[which] = 1
            else:
                genome[which] = 0

    return int(mutations)


# 2D Binary String

def G2DBinaryStringMutatorSwap(genome, **args):
    """ The mutator of G2DBinaryString, Swap Mutator

    .. versionadded:: 0.6
       The *G2DBinaryStringMutatorSwap* function
    """

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    if mutations < 1.0:
        mutations = 0
        for i in range(height):
            for j in range(width):
                if Util.randomFlipCoin(args["pmut"]):
                    index_b = (rand_randint(0, height - 1), rand_randint(0, width - 1))
                    Util.list2DSwapElement(genome.genomeString, (i, j), index_b)
                    mutations += 1
    else:
        for it in range(int(round(mutations))):
            index_a = (rand_randint(0, height - 1), rand_randint(0, width - 1))
            index_b = (rand_randint(0, height - 1), rand_randint(0, width - 1))
            Util.list2DSwapElement(genome.genomeString, index_a, index_b)

    return int(mutations)


def G2DBinaryStringMutatorFlip(genome, **args):
    """ A flip mutator for G2DBinaryString

    .. versionadded:: 0.6
       The *G2DBinaryStringMutatorFlip* function
    """
    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    if genome[i][j] == 0:
                        genome.setItem(i, j, 1)
                    else:
                        genome.setItem(i, j, 0)
                    mutations += 1
    else:  # TODO very suspicious branch

        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)

            if genome[i][j] == 0:
                genome.setItem(which_y, which_x, 1)
            else:
                genome.setItem(which_y, which_x, 0)

    return int(mutations)
