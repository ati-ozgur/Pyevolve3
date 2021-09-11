"""

:mod:`Initializators` -- initialization methods module
===================================================================

In this module we have the genetic operators of initialization for each
chromosome representation, the most part of initialization is done by
choosing random data.

.. note:: In Pyevolve, the Initializator defines the data type that will
          be used on the chromosome, for example, the :func:`G1DListInitializatorInteger`
          will initialize the G1DList with Integers.


"""

# 1D List

from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice
from .. import Util

def G1DListInitializatorAllele(genome, **args):
    """ Allele initialization function of G1DList

    To use this initializator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    """

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G1DListInitializatorAllele, you must specify the 'allele' parameter")

    genome.genomeList = [allele[i].getRandomAllele() for i in range(genome.getListSize())]


def G1DListInitializatorInteger(genome, **args):
    """ Integer initialization function of G1DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    range_min = genome.getParam("rangemin", 0)
    range_max = genome.getParam("rangemax", 100)

    genome.genomeList = [rand_randint(range_min, range_max) for i in range(genome.getListSize())]


def G1DListInitializatorReal(genome, **args):
    """ Real initialization function of G1DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    range_min = genome.getParam("rangemin", 0)
    range_max = genome.getParam("rangemax", 100)

    genome.genomeList = [rand_uniform(range_min, range_max) for i in range(genome.getListSize())]
