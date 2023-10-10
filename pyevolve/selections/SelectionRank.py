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

    x=population[selected]
    return  population[selected]


SelectorLinearRanking.cachePopID = None
SelectorLinearRanking.probabilityWeights = None

def SelectorExponentialRanking(population: GPopulation, **args):
    """ The Exponential Ranking Selector
       """
    c=0.9;
    popSize = len(population)
    if not population.sorted:
        population.sort()

    if args["popID"] != SelectorExponentialRanking.cachePopID:

        start = popSize
        prob_counts = [0] * popSize
        current_score = population.bestRaw().score
        for index in range(popSize):
            if population[index].score != current_score:
                start = start - 1
            prob_counts[index] = start

        prob_weights = [];
        for i in prob_counts:
            prob_weights.append(((c - 1) / ((pow(c, popSize)) - 1) * (pow(c, (popSize - i)))))
        SelectorExponentialRanking.cachePopID = args["popID"]
        SelectorExponentialRanking.probabilityWeights = prob_weights

    else:
        prob_weights = SelectorExponentialRanking.probabilityWeights

    selected = random.choices(list(range(popSize)), weights=prob_weights)[0]

    return population[selected]

SelectorExponentialRanking.probabilityWeights = None
SelectorExponentialRanking.cachePopID = None
def SelectorSplitRanking(population: GPopulation, **args):
        """ The Split Ranking Selector
        """
        lamda1 = 0.3;
        lamda2 = 0.7;
        popSize = len(population)
        if not population.sorted:
            population.sort()

        if args["popID"] != SelectorSplitRanking.cachePopID:

            start = popSize
            prob_counts = [0] * popSize
            current_score = population.bestRaw().score
            for index in range(popSize):
                if population[index].score != current_score:
                    start = start - 1
                prob_counts[index] = start

            prob_weights=[];
            for i in prob_counts:
                if(i<=popSize/2):
                    prob_weights.append(lamda1*((8*i)/popSize*(popSize+2)));
                else:
                    prob_weights.append(lamda2 * ((8 * i) / popSize * (3*popSize + 2)));
            SelectorSplitRanking.cachePopID = args["popID"]
            SelectorSplitRanking.probabilityWeights = prob_weights

        else:
            prob_weights = SelectorSplitRanking.probabilityWeights

        selected = random.choices(list(range(popSize)), weights=prob_weights)[0]

        return population[selected]

SelectorSplitRanking.probabilityWeights = None
SelectorSplitRanking.cachePopID = None