from random import randint as rand_randint, choice as rand_choice
from random import random as rand_random
import math
import random
from pyevolve.perturbations import DoublyCircularLinkedList as dcll
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
    """ The PMX Crossover for G1DList  (Partially Mapped Crossover)

    See more information in the `PMX Crossover Operator
    <https://www.researchgate.net/publication/335991207_Izmir_Iktisat_Dergisi_Gezgin_Satici_Probleminin_Genetik_Algoritmalar_Kullanarak_Cozumunde_Caprazlama_Operatorlerinin_Ornek_Olaylar_Bazli_Incelenmesi_Investigation_Of_Crossover_Operators_Using_Genetic_>`_
    """

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
    """ The Cycle Crossover for G1DList  (Cycle Crossover)

    See more information in the `Cycle Crossover Operator
    <https://www.researchgate.net/publication/335991207_Izmir_Iktisat_Dergisi_Gezgin_Satici_Probleminin_Genetik_Algoritmalar_Kullanarak_Cozumunde_Caprazlama_Operatorlerinin_Ornek_Olaylar_Bazli_Incelenmesi_Investigation_Of_Crossover_Operators_Using_Genetic_>`_
    """

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

def G1DListCrossoverOX2(genome, **args):
    """ Order-based (OX2) Crossover for G1DList  (Order-based (OX2) Crossover)

    See more information in the `Order-based (OX2) Crossover Operator
    <https://www.researchgate.net/publication/335991207_Izmir_Iktisat_Dergisi_Gezgin_Satici_Probleminin_Genetik_Algoritmalar_Kullanarak_Cozumunde_Caprazlama_Operatorlerinin_Ornek_Olaylar_Bazli_Incelenmesi_Investigation_Of_Crossover_Operators_Using_Genetic_>`_
    """

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)
    indexs=[]

    numberOfIndex = rand_randint(1, len(gMom) - 1)

    while len(indexs) < numberOfIndex:
        c2 = rand_randint(1, len(gMom) - 1)
        if c2 not in indexs:
            indexs.append(c2)

    indexs.sort();

    if args["count"] >= 1:

        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = [None] * len(gMom.genomeList)
        index=[None] * len(indexs)

        for i in range(0, len(gDad.genomeList)):
            sister.genomeList[i] = gDad.genomeList[i]

        for i in range(0, len(indexs)):
            for j in range(0, len(gMom.genomeList)):
                k = indexs[i];
                if gMom.genomeList[k] == gDad.genomeList[j]:
                    index[i] = j;
        index.sort();
        for j in range(0, len(index)):
            sister.genomeList[index[j]] = gMom.genomeList[indexs[j]];

    if args["count"] == 2:

        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = [None] * len(gDad.genomeList)
        index=[None] * len(indexs)

        for i in range(0, len(gMom.genomeList)):
            brother.genomeList[i] = gMom.genomeList[i]

        for i in range(0, len(indexs)):
            for j in range(0, len(gDad.genomeList)):
                k = indexs[i];
                if gDad.genomeList[k] == gMom.genomeList[j]:
                    index[i] = j;
        index.sort();
        for j in range(0, len(index)):
            brother.genomeList[index[j]] = gDad.genomeList[indexs[j]];

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def G1DListCrossoverPOS(genome, **args):
    """ Position-Based crossover (POS) Crossover for G1DList  (Position-Based (POS) Crossover)

    See more information in the `Position-Based (POS) Crossover Operator
    <https://www.researchgate.net/publication/335991207_Izmir_Iktisat_Dergisi_Gezgin_Satici_Probleminin_Genetik_Algoritmalar_Kullanarak_Cozumunde_Caprazlama_Operatorlerinin_Ornek_Olaylar_Bazli_Incelenmesi_Investigation_Of_Crossover_Operators_Using_Genetic_>`_
    """

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)
    indexs=[]

    numberOfIndex = rand_randint(1, len(gMom) - 1)

    while len(indexs) < numberOfIndex:
        c2 = rand_randint(1, len(gMom) - 1)
        if c2 not in indexs:
            indexs.append(c2)

    indexs.sort();

    if args["count"] >= 1:

        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = [None] * len(gMom.genomeList)
        temp = [None] * (len(indexs))
        temp2 = [None] * (len(gMom.genomeList) - len(indexs))

        for i in range(0, len(indexs)):
            sister.genomeList[indexs[i]] = gDad.genomeList[indexs[i]]

        h = 0;
        for i in range(0, len(gMom.genomeList)):
            for j in range(0, len(indexs)):
                if gMom.genomeList[i] == gDad.genomeList[indexs[j]]:
                    temp[h] = gDad.genomeList[indexs[j]]
                    h = h + 1;
        h = 0;
        for i in range(len(gMom.genomeList)):
            for j in range(len(temp)):
                if gMom.genomeList[i] == temp[j]:
                    break;
                if j == len(temp) - 1:
                    temp2[h] = gMom.genomeList[i];
                    h = h + 1;
        k = 0;
        for i in range(0, len(gMom.genomeList)):
            if sister.genomeList[i] == None:
                sister.genomeList[i] = temp2[k];
                k = k + 1;


    if args["count"] == 2:

        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = [None] * len(gDad.genomeList)
        temp = [None] * (len(indexs))
        temp2 = [None] * (len(gDad.genomeList) - len(indexs))

        for i in range(0, len(indexs)):
            brother.genomeList[indexs[i]] = gMom.genomeList[indexs[i]]

        h = 0;
        for i in range(0, len(gDad.genomeList)):
            for j in range(0, len(indexs)):
                if gDad.genomeList[i] == gMom.genomeList[indexs[j]]:
                    temp[h] = gMom.genomeList[indexs[j]]
                    h = h + 1;
        h = 0;
        for i in range(len(gDad.genomeList)):
            for j in range(len(temp)):
                if gDad.genomeList[i] == temp[j]:
                    break;
                if j == len(temp) - 1:
                    temp2[h] = gDad.genomeList[i];
                    h = h + 1;
        k = 0;
        for i in range(0, len(gDad.genomeList)):
            if brother.genomeList[i] == None:
                brother.genomeList[i] = temp2[k];
                k = k + 1;

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def G1DListCrossoverMPX(genome, **args):
    """ Maximal Preservative Crossover (MPX) for G1DList  (Maximal Preservative (MPX) Crossover)

    See more information in the `Maximal Preservative (MPX) Crossover Operator
    <https://www.researchgate.net/publication/335991207_Izmir_Iktisat_Dergisi_Gezgin_Satici_Probleminin_Genetik_Algoritmalar_Kullanarak_Cozumunde_Caprazlama_Operatorlerinin_Ornek_Olaylar_Bazli_Incelenmesi_Investigation_Of_Crossover_Operators_Using_Genetic_>`_
    """

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)
    indexs=[]

    c1, c2 = [rand_randint(1, len(gMom) - 1), rand_randint(1, len(gMom) - 1)]

    while c1 == c2:
        c2 = rand_randint(1, len(gMom) - 1)

    if c1 > c2:
        h = c1
        c1 = c2
        c2 = h

    length = c2-c1;

    while length >= 10:
        length=length/2;

    for i in range(c1, c1+length):
        indexs.append(i)

    if args["count"] >= 1:

        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = [None] * len(gMom.genomeList)
        temp = [None] * (len(indexs))
        temp2 = [None] * (len(gMom.genomeList) - len(indexs))
        # Copy a slice from first parent:
        for i in range(0, len(indexs)):
            sister.genomeList[i] = gMom.genomeList[indexs[i]]

        h = 0;
        for i in range(0, len(gMom.genomeList)):
            for j in range(0, len(indexs)):
                if gDad.genomeList[i] == gMom.genomeList[indexs[j]]:
                    temp[h] = i
                    h = h + 1;
        h = 0;
        for i in range(len(gMom.genomeList)):
            for j in range(len(temp)):
                if i == temp[j]:
                    break;
                if j == len(temp) - 1:
                    temp2[h] = gDad.genomeList[i];
                    h = h + 1;
        k = 0;
        for i in range(0, len(gMom.genomeList)):
            if sister.genomeList[i] == None:
                sister.genomeList[i] = temp2[k];
                k = k + 1;


    if args["count"] == 2:

        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = [None] * len(gMom.genomeList)
        temp = [None] * (len(indexs))
        temp2 = [None] * (len(gMom.genomeList) - len(indexs))
        # Copy a slice from first parent:
        for i in range(0, len(indexs)):
            brother.genomeList[i] = gDad.genomeList[indexs[i]]

        h = 0;
        for i in range(0, len(gDad.genomeList)):
            for j in range(0, len(indexs)):
                if gMom.genomeList[i] == gDad.genomeList[indexs[j]]:
                    temp[h] = i
                    h = h + 1;
        h = 0;
        for i in range(len(gDad.genomeList)):
            for j in range(len(temp)):
                if i == temp[j]:
                    break;
                if j == len(temp) - 1:
                    temp2[h] = gMom.genomeList[i];
                    h = h + 1;
        k = 0;
        for i in range(0, len(gDad.genomeList)):
            if brother.genomeList[i] == None:
                brother.genomeList[i] = temp2[k];
                k = k + 1;

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def G1DListCrossoverEPMX(genome, **args):
    """ The Extended PMX Crossover for G1DList  (Extended Partially Mapped Crossover)

    See more information in the `Extended PMX (EPMX) Crossover Operator
    <https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4666932>`_
    <https://www.researchgate.net/publication/260973230_Study_of_Some_Recent_Crossovers_Effects_on_Speed_and_Accuracy_of_Genetic_Algorithm_Using_Symmetric_Travelling_Salesman_Problem>`_
    """

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)

    c1 = rand_randint(1, len(gMom.genomeList) - 1)

    c2=listSize-c1;
    sister = gMom.clone()
    sister.resetStats()
    sister.genomeList = [None] * len(gMom.genomeList)
    motherSublist = [None] * (c1)
    motherSublist2 = [None] * (c2)

    brother = gDad.clone()
    brother.resetStats()
    brother.genomeList = [None] * len(gDad.genomeList)
    fatherSublist = [None] * (c1)
    fatherSublist2 = [None] *(c2)

    repeated = [];
    nonrepatedofMother = [];
    nonrepatedofFather = [];

    motherSublist[0:c1] = gMom.genomeList[0:c1];
    motherSublist2[0:c2] = gMom.genomeList[c1:len(gMom.genomeList)];
    fatherSublist[0:c1] = gDad.genomeList[0:c1];
    fatherSublist2[0:c2] = gDad.genomeList[c1:len(gDad.genomeList)];

    for i in range(0, len(motherSublist)):
        for j in range(0, len(fatherSublist)):
            if motherSublist[i] == fatherSublist[j]:
                repeated.append(motherSublist[i]);

    nonrepatedofFather = motherSublist[:]
    nonrepatedofMother = fatherSublist[:]

    for i in range(0, len(repeated)):
        nonrepatedofFather.remove(repeated[i])
        nonrepatedofMother.remove(repeated[i])

    for i in range(0, len(motherSublist2)):
        for j in range(0, len(nonrepatedofMother)):
            if (motherSublist2[i] == nonrepatedofMother[j]):
                motherSublist2[i] = nonrepatedofFather[j];

    for i in range(0, len(motherSublist2)):
        for j in range(0, len(nonrepatedofMother)):
            if (fatherSublist2[i] == nonrepatedofFather[j]):
                fatherSublist2[i] = nonrepatedofMother[j];

    sister.genomeList = motherSublist + fatherSublist2;
    brother.genomeList = fatherSublist + motherSublist2;

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def G1DListCrossoverGreedy(genome, **args):
    """ The Greedy Crossover(GX) for G1DList  (Greedy Crossover)

    See more information in the `Greedy Crossover (GX) Crossover Operator
    <https://polen.itu.edu.tr/bitstream/11527/413/1/13612.pdf>`_
    <https://arxiv.org/ftp/arxiv/papers/1209/1209.5339.pdf>`_
    <https://www.researchgate.net/publication/260973230_Study_of_Some_Recent_Crossovers_Effects_on_Speed_and_Accuracy_of_Genetic_Algorithm_Using_Symmetric_Travelling_Salesman_Problem>`_
    """

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)

    distance = None
    distance= gMom.internalParams;
    dist=dictionaryToMatrix(distance)

    c1Inital = rand_randint(0, len(gMom.genomeList) - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = [None] * len(gMom.genomeList)
        c1 = c1Inital
        c2 = findIndex(gDad.genomeList, gMom.genomeList[c1]);
        sister.genomeList[0] = gMom.genomeList[c1]
        k = 1;

        while None in sister.genomeList:

            if dist[(gMom.genomeList[c1 % listSize] - 1)] [(gMom.genomeList[(c1 + 1) % listSize] - 1)] > dist[(gDad.genomeList[c2 % listSize] - 1)] [(gDad.genomeList[(c2 + 1) % listSize] - 1)]:

                bool1 = findIndex(sister.genomeList, gMom.genomeList[(c1 + 1) % listSize]);
                bool2 = findIndex(sister.genomeList, gDad.genomeList[(c2 + 1) % listSize]);

                if bool1 == None:
                    sister.genomeList[k] = gMom.genomeList[(c1 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, sister.genomeList[k])
                    c2 = findIndex(gDad.genomeList, sister.genomeList[k])
                    k = k + 1;
                elif bool2 == None:
                    sister.genomeList[k] = gDad.genomeList[(c2 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, sister.genomeList[k])
                    c2 = findIndex(gDad.genomeList, sister.genomeList[k])
                    k = k + 1;
                else:
                    c1 = c1 + 1;
                    c2 = findIndex(gDad.genomeList, gMom.genomeList[c1 % listSize]);
            else:
                bool1 = findIndex(sister.genomeList, gMom.genomeList[(c1 + 1) % listSize]);
                bool2 = findIndex(sister.genomeList, gDad.genomeList[(c2 + 1) % listSize]);

                if bool2 == None:
                    sister.genomeList[k] = gDad.genomeList[(c2 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, sister.genomeList[k])
                    c2 = findIndex(gDad.genomeList, sister.genomeList[k])
                    k = k + 1;
                elif bool1 == None:
                    sister.genomeList[k] = gMom.genomeList[(c1 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, sister.genomeList[k])
                    c2 = findIndex(gDad.genomeList, sister.genomeList[k])
                    k = k + 1;
                else:
                    c1 = c1 + 1;
                    c2 = findIndex(gDad.genomeList, gMom.genomeList[c1 % listSize]);

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = [None] * len(gMom.genomeList)
        gMom.genomeList.reverse();
        gDad.genomeList.reverse();
        c1=c1Inital;
        c2 = findIndex(gDad.genomeList, gMom.genomeList[c1]);
        brother.genomeList[0] = gMom.genomeList[c1]
        k = 1;

        while None in brother.genomeList:

            if dist[(gMom.genomeList[c1 % listSize] - 1)][(gMom.genomeList[(c1 + 1) % listSize] - 1)] < dist[(gDad.genomeList[c2 % listSize] - 1)][(gDad.genomeList[(c2 + 1) % listSize] - 1)]:

                bool1 = findIndex(brother.genomeList, gMom.genomeList[(c1 + 1) % listSize]);
                bool2 = findIndex(brother.genomeList, gDad.genomeList[(c2 + 1) % listSize]);

                if bool1 == None:
                    brother.genomeList[k] = gMom[(c1 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, brother.genomeList[k])
                    c2 = findIndex(gDad.genomeList, brother.genomeList[k])
                    k = k + 1;
                elif bool2 == None:
                    brother.genomeList[k] = gDad.genomeList[(c2 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, brother.genomeList[k])
                    c2 = findIndex(gDad.genomeList, brother.genomeList[k])
                    k = k + 1;
                else:
                    c1 = c1 + 1;
                    c2 = findIndex(gDad.genomeList, gMom.genomeList[c1 % listSize]);
            else:
                bool1 = findIndex(brother.genomeList, gMom.genomeList[(c1 + 1) % listSize]);
                bool2 = findIndex(brother.genomeList, gDad.genomeList[(c2 + 1) % listSize]);

                if bool2 == None:
                    brother.genomeList[k] = gDad.genomeList[(c2 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, brother.genomeList[k])
                    c2 = findIndex(gDad.genomeList, brother.genomeList[k])
                    k = k + 1;
                elif bool1 == None:
                    brother.genomeList[k] = gMom.genomeList[(c1 + 1) % listSize];
                    c1 = findIndex(gMom.genomeList, brother.genomeList[k])
                    c2 = findIndex(gDad.genomeList, brother.genomeList[k])
                    k = k + 1;
                else:
                    c1 = c1 + 1;
                    c2 = findIndex(gDad.genomeList, gMom.genomeList[c1 % listSize]);

    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def G1DListCrossoverIGX(genome, **args):
    """ The Improved Greedy Crossover(IGX) for G1DList  (Improved Greedy Crossover)

    See more information in the `Impoved Greedy Crossover (IGX) Crossover Operator
    <https://arxiv.org/ftp/arxiv/papers/1209/1209.5339.pdf>`_
    """

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    listSize = len(gMom)

    distance = None
    distance= gMom.internalParams;
    dist=dictionaryToMatrix(distance)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister.genomeList = [None] * len(gMom.genomeList)
        stepcounter = len(gDad.genomeList)
        sisterGenome = []

        fatherdll = dcll.DCLL()
        for i in range(0, len(gDad.genomeList)):
            fatherdll.append(gDad.genomeList[i])

        motherdll = dcll.DCLL()
        for i in range(0, len(gMom.genomeList)):
            motherdll.append(gMom.genomeList[i])

        for i in range(0, len(gMom.genomeList) - 1):
            if i == 0:
                first = random.choice(gDad.genomeList)
                ind = fatherdll.getindex(stepcounter, first)
                indm = motherdll.getindex(stepcounter, first)

                t = []
                fneighs = fatherdll.getleftright(stepcounter, first)
                mneighs = motherdll.getleftright(stepcounter, first)

                t.append(fneighs)
                t.append(mneighs)
                candidateslist = [item for sublist in t for item in sublist]
                for i in range(0, len(candidateslist)):
                    val = dist[(first % stepcounter) - 1][(candidateslist[i] % stepcounter) - 1]
                    if i == 0:
                        mindistance = val
                        vertice = candidateslist[i]
                    else:
                        if val < mindistance:
                            mindistance = val
                            vertice = candidateslist[i]

                sisterGenome.append(first)
                stepcounter = stepcounter - 1
                fatherdll.remove(ind)
                motherdll.remove(indm)
                sisterGenome.append(vertice)
            else:
                ind = fatherdll.getindex(stepcounter, vertice)
                indm = motherdll.getindex(stepcounter, vertice)
                t = []
                fneighs = fatherdll.getleftright(stepcounter, vertice)
                mneighs = motherdll.getleftright(stepcounter, vertice)
                t.append(fneighs)
                t.append(mneighs)
                candidateslist = [item for sublist in t for item in sublist]
                verttemp = vertice
                for i in range(0, len(candidateslist)):
                    val = dist[(verttemp % stepcounter) - 1][(candidateslist[i] % stepcounter) - 1]
                    if i == 0:
                        mindistance = val
                        vertice = candidateslist[i]
                    else:
                        if val < mindistance:
                            mindistance = val
                            vertice = candidateslist[i]
                sisterGenome.append(vertice)
                stepcounter = stepcounter - 1
                fatherdll.remove(ind)
                motherdll.remove(indm)
        sister.genomeList=sisterGenome

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother.genomeList = [None] * len(gMom.genomeList)
        gMom.genomeList.reverse();
        gDad.genomeList.reverse();
        stepcounter = len(gDad.genomeList)
        brotherGenome = []
        fatherdll = dcll.DCLL()
        for i in range(0, len(gDad.genomeList)):
            fatherdll.append(gDad.genomeList[i])

        motherdll = dcll.DCLL()
        for i in range(0, len(gMom.genomeList)):
            motherdll.append(gMom.genomeList[i])

        for i in range(0, len(gMom.genomeList) - 1):
            if i == 0:
                first = random.choice(gDad.genomeList)
                ind = fatherdll.getindex(stepcounter, first)
                indm = motherdll.getindex(stepcounter, first)

                t = []
                fneighs = fatherdll.getleftright(stepcounter, first)
                mneighs = motherdll.getleftright(stepcounter, first)

                t.append(fneighs)
                t.append(mneighs)
                candidateslist = [item for sublist in t for item in sublist]
                for i in range(0, len(candidateslist)):
                    val = dist[(first % stepcounter) - 1][(candidateslist[i] % stepcounter) - 1]
                    if i == 0:
                        mindistance = val
                        vertice = candidateslist[i]
                    else:
                        if val > mindistance:
                            mindistance = val
                            vertice = candidateslist[i]

                brotherGenome.append(first)
                stepcounter = stepcounter - 1
                fatherdll.remove(ind)
                motherdll.remove(indm)
                brotherGenome.append(vertice)
            else:
                ind = fatherdll.getindex(stepcounter, vertice)
                indm = motherdll.getindex(stepcounter, vertice)
                t = []
                fneighs = fatherdll.getleftright(stepcounter, vertice)
                mneighs = motherdll.getleftright(stepcounter, vertice)
                t.append(fneighs)
                t.append(mneighs)
                candidateslist = [item for sublist in t for item in sublist]
                verttemp = vertice
                for i in range(0, len(candidateslist)):
                    val = dist[(verttemp % stepcounter) - 1][(candidateslist[i] % stepcounter) - 1]
                    if i == 0:
                        mindistance = val
                        vertice = candidateslist[i]
                    else:
                        if val < mindistance:
                            mindistance = val
                            vertice = candidateslist[i]
                brotherGenome.append(vertice)
                stepcounter = stepcounter - 1
                fatherdll.remove(ind)
                motherdll.remove(indm)
        brother.genomeList=brotherGenome
    assert listSize == len(sister)
    assert listSize == len(brother)

    return (sister, brother)

def findIndex(array,number):

    index=None;
    for i in range(0, len(array)):
        if array[i] == number:
            index=i;
    return index

def dictionaryToMatrix(distance):

    List=list(distance.values())
    temp_x, temp_y = map(max, zip(*List[0]))
    matrix = [[List[0].get((j, i), 0) for i in range(temp_y + 1)]
           for j in range(temp_x + 1)]
    return matrix