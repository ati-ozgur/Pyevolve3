from random import randint as rand_randint, choice as rand_choice
from random import random as rand_random
import math
from .. import Util



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

def G1DListCrossoverPMX(genome, **args):
    """ The PMX Crossover for G1DList  (Partially Mapped Crossover) """
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
        sister.genomeList=[None]*len(gMom.genomeList)
        # Copy a slice from first parent:
        sister.genomeList[c1:c2] = gMom.genomeList[c1:c2]
        #    Map the same slice in parent b to child using indices from parent a:
        for ind, x in enumerate(gDad.genomeList[c1:c2]):
            ind += c1
            if x not in sister.genomeList:
                while sister.genomeList[ind] != None:
                    ind = gDad.genomeList.index(gMom.genomeList[ind])
                sister.genomeList[ind] = x
        # Copy over the rest from parent b
        for ind, x in enumerate(sister.genomeList):
            if x == None:
                sister.genomeList[ind] = gDad.genomeList[ind]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList=[None]*len(gDad.genomeList)
        # Copy a slice from first parent:
        brother.genomeList[c1:c2] = gDad.genomeList[c1:c2]
        #    Map the same slice in parent b to child using indices from parent a:
        for ind, x in enumerate(gMom.genomeList[c1:c2]):
            ind += c1
            if x not in brother.genomeList:
                while brother.genomeList[ind] != None:
                    ind = gMom.genomeList.index(gDad.genomeList[ind])
                brother.genomeList[ind] = x
        # Copy over the rest from parent b
        for ind, x in enumerate(brother.genomeList):
            if x == None:
                brother.genomeList[ind] = gMom.genomeList[ind]

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def G1DListCrossoverCycle(genome, **args):
    """ The Cycle Crossover for G1DList  (Cycle Crossover) """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = [None] * len(gMom.genomeList)
        while None in sister.genomeList:
            ind = sister.genomeList.index(None)
            indices = []
            values = []
            while ind not in indices:
                val = gMom.genomeList[ind]
                indices.append(ind)
                values.append(val)
                ind = gMom.genomeList.index(gDad.genomeList[ind])
            for ind, val in zip(indices, values):
                sister.genomeList[ind] = val
            gMom.genomeList, gDad.genomeList = gDad.genomeList, gMom.genomeList

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = [None] * len(gDad.genomeList)
        while None in brother.genomeList:
            ind = brother.genomeList.index(None)
            indices = []
            values = []
            while ind not in indices:
                val = gDad.genomeList[ind]
                indices.append(ind)
                values.append(val)
                ind = gDad.genomeList.index(gMom.genomeList[ind])
            for ind, val in zip(indices, values):
                brother.genomeList[ind] = val
            gDad.genomeList, gMom.genomeList = gMom.genomeList, gDad.genomeList

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)
