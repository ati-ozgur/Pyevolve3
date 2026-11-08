from pyevolve.representations.G1DList import G1DList
from pyevolve.initializations.InitializationG1DList import G1DListInitializatorReal
from pyevolve.perturbations.MutatorG1DList import G1DListMutatorRealGaussian
from pyevolve import GSimpleGA
from pyevolve import Scaling
from pyevolve.selections import Selectors

from pyevolve import Consts


def putnam_b1(genome):
    x = genome[0]
    numerator = (x + 1 / x) ** 6 - (x**6 + 1 / x**6) - 2
    denominator = (x + 1 / x) ** 3 + (x**3 + 1 / x**3)
    f = numerator / denominator
    return f


r"""

\text{Find the minimum value of}
\[
\frac{(x + 1/x)^6 - (x^6 + 1/x^6) - 2}{(x + 1/x)^3 + (x^3 + 1/x^3)}
\]
See following video: https://youtu.be/TZnXbOhRVws
"""


def run_main():
    # Genome instance
    genome = G1DList(1)
    genome.setParams(rangemin=-100.0, rangemax=100.0, bestrawscore=0.0000, rounddecimal=4)
    genome.initializator.set(G1DListInitializatorReal)
    genome.mutator.set(G1DListMutatorRealGaussian)

    # The evaluator function (objective function)
    genome.evaluator.set(putnam_b1)
    # since there is only one element, crossover is not needed
    genome.crossover.clear()

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.selector.set(Selectors.GRouletteWheel)

    ga.setMinimax(Consts.minimaxType["minimize"])

    pop = ga.getPopulation()
    pop.scaleMethod.set(Scaling.SigmaTruncScaling)

    ga.setGenerations(8000)
    ga.setMutationRate(0.05)
    ga.setPopulationSize(100)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=250)

    # Best individual
    best = ga.bestIndividual()
    print(best)
    print("Best individual score: %.2f" % best.getRawScore())


if __name__ == "__main__":
    run_main()
