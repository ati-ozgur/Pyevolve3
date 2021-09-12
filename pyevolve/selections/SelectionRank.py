import random
from .. import Consts
from ..GPopulation import GPopulation


def SelectorLinearRanking(population: GPopulation, **args):
    """ The Linear Ranking Selector 
    """
    popSize = len(population)
    if not population.sorted:
        population.sort()

    if args["popID"] != SelectorLinearRanking.cachePopID:
        
        start = popSize
        prob_counts = [0] * popSize
        current_score = population.bestRaw().score
        for index in range(popSize):
            if population[index].score != current_score:
                start = start - 1
            prob_counts[index] = start

        total = sum(prob_counts)
        prob_weights = [a/total for a in prob_counts]
        SelectorLinearRanking.cachePopID = args["popID"]
        SelectorLinearRanking.probabilityWeights = prob_weights

    else:
        prob_weights = SelectorLinearRanking.probabilityWeights


    selected = random.choices(list(range(popSize)),weights=prob_weights)[0]
    return  population[selected]


SelectorLinearRanking.cachePopID = None
SelectorLinearRanking.probabilityWeights = None
