from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice
from .. import Util
# 1D Binary String


def G1DBinaryStringInitializator(genome, **args):
    """ 1D Binary String initializator """
    genome.genomeList = [rand_choice((0, 1)) for _ in range(genome.getListSize())]


# 2D Binary String

def G2DBinaryStringInitializator(genome, **args):
    """ Integer initialization function of 2D Binary String

    .. versionadded:: 0.6
       The *G2DBinaryStringInitializator* function
    """
    genome.clearString()

    for i in range(genome.getHeight()):
        for j in range(genome.getWidth()):
            random_gene = rand_choice((0, 1))
            genome.setItem(i, j, random_gene)
