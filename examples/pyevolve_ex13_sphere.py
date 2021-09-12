from pyevolve.representations import G1DList
from pyevolve.initializations.InitializationG1DList import G1DListInitializatorReal
from pyevolve.perturbations.MutatorG1DList import G1DListMutatorRealGaussian
from pyevolve import GSimpleGA, Consts


# This is the Sphere Function
def sphere(xlist):
    total = 0
    for i in xlist:
        total += i**2
    return total


def run_main():
    genome = G1DList.G1DList(140)
    genome.setParams(rangemin=-5.12, rangemax=5.13)
    genome.initializator.set(G1DListInitializatorReal)
    genome.mutator.set(G1DListMutatorRealGaussian)
    genome.evaluator.set(sphere)

    ga = GSimpleGA.GSimpleGA(genome, seed=666)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(1500)
    ga.setMutationRate(0.01)
    ga.evolve(freq_stats=500)


if __name__ == "__main__":
    run_main()
