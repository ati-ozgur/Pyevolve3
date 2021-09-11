
import pyevolve
from pyevolve.representations.G1DList import G1DList
from pyevolve import GSimpleGA
from pyevolve.selections import Selectors
from pyevolve import DBAdapters


# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(genome):
    score = 0.0

    # iterate over the chromosome
    # The same as "score = len(filter(lambda x: x==0, genome))"
    for value in genome:
        if value == 0:
            score += 1

    return score


def run_main():
    # Genome instance, 1D List of 50 elements
    genome = G1DList(50)

    # Sets the range max and min of the 1D List
    genome.setParams(rangemin=0, rangemax=10)

    # The evaluator function (evaluation function)
    genome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)

    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(500)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)


    # Do the evolution, with stats dump
    # frequency of 20 generations
    best_individual = ga.evolve(freq_stats=20)

    # Best individual
    print(best_individual)


if __name__ == "__main__":
    run_main()
