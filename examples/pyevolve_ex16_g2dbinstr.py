from pyevolve.representations import G2DBinaryString
from pyevolve import GSimpleGA
from pyevolve.perturbations.CrossoverBinary import G2DBinaryStringXSingleHPoint
from pyevolve.perturbations.MutatorBinary import G2DBinaryStringMutatorSwap


# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
    score = 0.0

    # iterate over the chromosome
    for i in range(chromosome.getHeight()):
        for j in range(chromosome.getWidth()):
            # You can use the chromosome.getItem(i, j)
            if chromosome[i][j] == 0:
                score += 0.1
    return score


# Genome instance
genome = G2DBinaryString.G2DBinaryString(8, 5)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)
genome.crossover.set(G2DBinaryStringXSingleHPoint)
genome.mutator.set(G2DBinaryStringMutatorSwap)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.setGenerations(200)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=10)

# Best individual
print(ga.bestIndividual())
