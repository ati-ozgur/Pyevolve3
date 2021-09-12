from pyevolve.representations import G1DList,
from pyevolve.initializations.InitializationG1DList import G1DListInitializatorReal
from pyevolve.perturbations.MutatorG1DList import G1DListMutatorRealRange
from pyevolve import GSimpleGA,  Consts
from pyevolve.selections import Selectors

# This is the Rosenbrock Function
def rosenbrock(xlist):
    sum_var = 0
    for x in range(1, len(xlist)):
        sum_var += 100.0 * (xlist[x] - xlist[x - 1]**2)**2 + (1 - xlist[x - 1])**2
    return sum_var


def run_main():
    # Genome instance
    genome = G1DList.G1DList(15)
    genome.setParams(rangemin=-1, rangemax=1.1)
    genome.initializator.set(G1DListInitializatorReal)
    genome.mutator.set(G1DListMutatorRealRange)

    # The evaluator function (objective function)
    genome.evaluator.set(rosenbrock)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(4000)
    ga.setCrossoverRate(0.9)
    ga.setPopulationSize(100)
    ga.setMutationRate(0.03)

    ga.evolve(freq_stats=500)

    # Best individual
    best = ga.bestIndividual()
    print("\nBest individual score: %.2f" % (best.score,))
    print(best)


if __name__ == "__main__":
    run_main()
