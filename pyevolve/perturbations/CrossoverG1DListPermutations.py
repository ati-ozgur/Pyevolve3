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
