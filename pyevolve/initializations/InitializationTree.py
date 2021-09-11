# Tree


from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice
from ..representations import GTree
from . import Util


def GTreeInitializatorInteger(genome, **args):
    """ Integer initialization function of GTree

    This initializator accepts the *rangemin* and *rangemax* genome parameters.
    It accepts the following parameters too:

    *max_depth*
       The max depth of the tree

    *max_siblings*
       The number of maximum siblings of an node

    *method*
       The method, accepts "grow", "full" or "ramped".

    .. versionadded:: 0.6
       The *GTreeInitializatorInteger* function.
    """
    max_depth = genome.getParam("max_depth", 5)
    max_siblings = genome.getParam("max_siblings", 2)

    range_min = genome.getParam("rangemin", 0)
    range_max = genome.getParam("rangemax", 100)

    def lambda_generator():
        return rand_randint(range_min, range_max)

    method = genome.getParam("method", "grow")

    if method == "grow":
        root = GTree.buildGTreeGrow(0, lambda_generator, max_siblings, max_depth)
    elif method == "full":
        root = GTree.buildGTreeFull(0, lambda_generator, max_siblings, max_depth)
    elif method == "ramped":
        if Util.randomFlipCoin(0.5):
            root = GTree.buildGTreeGrow(0, lambda_generator, max_siblings, max_depth)
        else:
            root = GTree.buildGTreeFull(0, lambda_generator, max_siblings, max_depth)
    else:
        Util.raiseException("Unknown tree initialization method [%s] !" % method)

    genome.setRoot(root)  # TODO probably additional check needed
    genome.processNodes()
    assert genome.getHeight() <= max_depth


def GTreeInitializatorAllele(genome, **args):
    """ Allele initialization function of GTree

    To use this initializator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    .. warning:: the :class:`GAllele.GAlleles` instance **must** have the homogeneous flag enabled

    .. versionadded:: 0.6
       The *GTreeInitializatorAllele* function.
    """
    max_depth = genome.getParam("max_depth", 5)
    max_siblings = genome.getParam("max_siblings", 2)
    method = genome.getParam("method", "grow")

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the GTreeInitializatorAllele, you must specify the 'allele' parameter")

    if not allele.homogeneous:
        Util.raiseException("to use the GTreeInitializatorAllele, the 'allele' must be homogeneous")

    if method == "grow":
        root = GTree.buildGTreeGrow(0, allele[0].getRandomAllele, max_siblings, max_depth)
    elif method == "full":
        root = GTree.buildGTreeFull(0, allele[0].getRandomAllele, max_siblings, max_depth)
    elif method == "ramped":
        if Util.randomFlipCoin(0.5):
            root = GTree.buildGTreeGrow(0, allele[0].getRandomAllele, max_siblings, max_depth)
        else:
            root = GTree.buildGTreeFull(0, allele[0].getRandomAllele, max_siblings, max_depth)
    else:
        Util.raiseException("Unknown tree initialization method [%s] !" % method)

    genome.setRoot(root)
    genome.processNodes()
    assert genome.getHeight() <= max_depth


# Tree GP   ##

def GTreeGPInitializator(genome, **args):
    """This initializator accepts the follow parameters:

    *max_depth*
       The max depth of the tree

    *method*
       The method, accepts "grow", "full" or "ramped"

    .. versionadded:: 0.6
       The *GTreeGPInitializator* function.
    """

    max_depth = genome.getParam("max_depth", 5)
    method = genome.getParam("method", "grow")
    ga_engine = args["ga_engine"]

    if method == "grow":
        root = GTree.buildGTreeGPGrow(ga_engine, 0, max_depth)
    elif method == "full":
        root = GTree.buildGTreeGPFull(ga_engine, 0, max_depth)
    elif method == "ramped":
        if Util.randomFlipCoin(0.5):
            root = GTree.buildGTreeGPFull(ga_engine, 0, max_depth)
        else:
            root = GTree.buildGTreeGPGrow(ga_engine, 0, max_depth)
    else:
        Util.raiseException("Unknown tree initialization method [%s] !" % method)

    genome.setRoot(root)
    genome.processNodes()
    assert genome.getHeight() <= max_depth
