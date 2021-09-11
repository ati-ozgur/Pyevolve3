import random

def G1DListTSPInitializatorRandom(genome, **args):
    """ The initializator for the TSP """
    lst = [i for i in range(genome.getListSize())]
    random.shuffle(lst)
    genome.setInternalList(lst)
