# 2D List

def G2DListInitializatorInteger(genome, **args):
    """ Integer initialization function of G2DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    genome.clearList()

    for i in range(genome.getHeight()):
        for j in range(genome.getWidth()):
            randomInteger = rand_randint(genome.getParam("rangemin", 0),
                                         genome.getParam("rangemax", 100))
            genome.setItem(i, j, randomInteger)


def G2DListInitializatorReal(genome, **args):
    """ Integer initialization function of G2DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    genome.clearList()

    for i in range(genome.getHeight()):
        for j in range(genome.getWidth()):
            randomReal = rand_uniform(genome.getParam("rangemin", 0),
                                      genome.getParam("rangemax", 100))
            genome.setItem(i, j, randomReal)


def G2DListInitializatorAllele(genome, **args):
    """ Allele initialization function of G2DList

    To use this initializator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    .. warning:: the :class:`GAllele.GAlleles` instance must have the homogeneous flag enabled

    """

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G2DListInitializatorAllele, you must specify the 'allele' parameter")

    if not allele.homogeneous:
        Util.raiseException("to use the G2DListInitializatorAllele, the 'allele' must be homogeneous")

    genome.clearList()

    for i in range(genome.getHeight()):
        for j in range(genome.getWidth()):
            random_allele = allele[0].getRandomAllele()
            genome.setItem(i, j, random_allele)
