from pyevolve.GPopulation import GPopulation
from pyevolve.representations import G1DList
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



def create_initial_population(genome,size=10):
    genome_size = len(genome)
    population = []
    for i in range(size):
        val = i + 1
        inner_list = [val] * genome_size
        genome_init = genome.clone()
        genome_init.setInternalList(inner_list)
        population.append(genome_init)

    return population

def run_main():
    genome_size=50
    # Genome instance, 1D List of 50 elements
    genome = G1DList.G1DList(genome_size)

    # Sets the range max and min of the 1D List
    genome.setParams(rangemin=0, rangemax=10)

    # The evaluator function (evaluation function)
    genome.evaluator.set(eval_func)


    #GPopulation initPopulation

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)

    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(500)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)


    init_population = create_initial_population(genome)

    ga.getPopulation().setInitialPopulation(init_population)


    # Do the evolution, with stats dump
    # frequency of 20 generations
    best_individual = ga.evolve(freq_stats=20)

    # Best individual
    print(best_individual)


if __name__ == "__main__":
    run_main()
