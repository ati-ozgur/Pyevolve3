# Get Started - Tutorial

Pyevolve combined with the Python language can be a powerful tool. The best way to show you how Pyevolve can be used is to begin with some simple examples; later we'll show some snippets, etc. so you'll be alble to walk by yourself.

## First Example

To make the API easy to use, we have provided default values for almost every parameter in Pyevolve.
For example, when you use the `G1DList.G1DList` genome without specifying the Mutator, Crossover and Initializator, you will be using the default ones: Swap Mutator, One Point Crossover and the Integer Initialzator. All those default parameters are specified in the `Consts` module (and you are highly encouraged to take a look at source code).

Let's begin with the first simple example (Ex. 1). First of all, you must know your problem: in this case, our problem is to find a simple 1D list of integers of *n*-size with zero in all positions.
At first look, we know by intuition that the representation needed for this
problem is a 1D List, which you can find in Pyevolve by the name of `G1DList.G1DList`, which means Genome 1D List. This representation is based on a python list as you will see, and is very easy to manipulate.
The next step is to define the `evaluation function` to our Genetic Algorithm. We want all the *n* list positions with value of '0', so we can propose the evaluation function:

![](imgs/ex1equation.png){fig-align="center"}

As you can see in the above equation, with the *x* variable representing our genome list of integers, the *f(x)* shows our evaluation function, which is the sum of '0' values in the list. For example, if we have a list with 10 elements like this:

```
x = [1, 2, 3, 8, 0, 2, 0, 4, 1, 0]
```

we will get the raw score [^rawscore] value of 3, or *f(x)* = 3. It's very simple to understand. Now, let's code this.

We will define our `evaluation function` **"eval_func"** as:

```
# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0

   # iterate over the chromosome elements (items)
   for value in chromosome:
      if value==0:
         score += 1.0

   return score
```

As you can see, this evaluation function tests each element in the list for equality with '0' and returns the proportional score value. The `G1DList.G1DList` chromosome is not a python list by itself but it encapsulates one and exposes the methods for this list, like the iterator used in the above loop.
The next step is the creation of a `sample genome` [^samplegenome] for the Genetic Algorithm. We can define our genome as this:

```
# Genome instance
genome = G1DList.G1DList(20)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)
```

This will create an instance of the `G1DList.G1DList` class (which resides in the `G1DList` module) with the list *n*-size of 20 and sets the evaluation function of the genome to the evaluation function **"eval_func"** that we created before.

But wait - where is the range of integers that will be used in the list? Where are the mutator, crossover and initialization functions? They are all set to their default parameters. Using these parameters keep things simple.

By default (and you have the **documentation** to find these defaults), the range of the integers in the `G1DList.G1DList` is between the inverval \[ `Consts.CDefRangeMin`, `Consts.CDefRangeMax`\] inclusive, and genetic operators is the same I have cited before: Swap Mutator `Mutators.G1DListMutatorSwap`, One Point Crossover `Crossovers.G1DListCrossoverSinglePoint` and the Integer Initializator `Initializators.G1DListInitializatorInteger`. You can change everything with the API. For example, you can pass the ranges to the genome like so:

```
genome.setParams(rangemin=0, rangemax=10)
```

Right, now that we have our evaluation function and our first genome ready, the next step is to create our Genetic Algorithm Engine, the GA Core which will do the evolution, control statistics, etc...
The GA Engine which we will use is the `GSimpleGA.GSimpleGA` which resides in the `GSimpleGA` module. This GA Engine is the genetic algorithm [^ganote] described by Goldberg. So, let's create the engine:

```
ga = GSimpleGA.GSimpleGA(genome)
```

The GA is now ready to use. We have simply created our GA Engine with the previously created genome. You might be asking: "*Where did we set the selector method, the number of generations, and the mutation rate?*". Again: we are using the default settings. By default, the GA will evolve for 100 generations with a population size of 80 individuals, it will use the mutation rate of 2% (there is a 2% chance that each individual created in a generation is mutated using the chosen mutation operator) and a crossover rate of 80% (there is an 80% chance that each individual created in a generation is created using the chosen crossover operator), the default selector is the Ranking Selection (`Selectors.GRankSelector`) method. Those default parameters were not picked at random, they are all based on the commonly used settings.

Now, all we need to do is to evolve the population!

```
# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=10)

# Best individual
print ga.bestIndividual()
```

::: {.callout-note}
Pyevolve have the \_\_repr\_\_() function implemented for almost all objects, this means that you
can use syntax like 'print object' and the object information will be show in an
pretty format.
:::

Ready, now we have our first Genetic Algorithm. It looks more like a "Hello GA!" application. The code above shows the call of
the `GSimpleGA.GSimpleGA.evolve` method, with the parameter *freq_stats=10*. This method will do the evolution and will show the statistics every 10th generation. The next method called is the `GSimpleGA.GSimpleGA.bestIndividual`. This method will return the best individual after the end of the evolution, and with the *print* python command, the genome is shown on the screen.

When running the code, this is the resulting output:

```
Gen. 1 (1.00%): Max/Min/Avg Fitness(Raw)     [2.40(3.00)   / 1.60(1.00)   /   2.00(2.00)]
Gen. 10 (10.00%): Max/Min/Avg Fitness(Raw)   [10.80(10.00) / 7.20(8.00)   /   9.00(9.00)]
Gen. 20 (20.00%): Max/Min/Avg Fitness(Raw)   [22.80(20.00) / 15.20(18.00) / 19.00(19.00)]
Gen. 30 (30.00%): Max/Min/Avg Fitness(Raw)   [20.00(20.00) / 20.00(20.00) / 20.00(20.00)]
                 (...)
Gen. 100 (100.00%): Max/Min/Avg Fitness(Raw) [20.00(20.00) / 20.00(20.00) / 20.00(20.00)]

Total time elapsed: 3.375 seconds.

- GenomeBase
        Score:                   20.000000
        Fitness:                 20.000000

        Slot [Evaluator] (Count: 1)
                Name: eval_func
        Slot [Initializator] (Count: 1)
                Name: G1DListInitializatorInteger
                Doc:  Integer initialization function of G1DList,
                      accepts 'rangemin' and 'rangemax'
        Slot [Mutator] (Count: 1)
                Name: G1DListMutatorSwap
                Doc:  The mutator of G1DList, Swap Mutator
        Slot [Crossover] (Count: 1)
                Name: G1DListCrossoverSinglePoint
                Doc:  The crossover of G1DList, Single Point
- G1DList
        List size:       20
        List:            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

This is the evolution of our Genetic Algorithm, with the best individual shown at the end of the evolution. As you can see, the population obtained the best raw score (20.00) near generation 20.

### Final source code

Here is the final source code:

```
from pyevolve.representations import G1DList
from pyevolve import GSimpleGA

def eval_func(chromosome):
   score = 0.0
   # iterate over the chromosome
   for value in chromosome:
      if value==0:
         score += 1
   return score

genome = G1DList.G1DList(20)
genome.evaluator.set(eval_func)
ga = GSimpleGA.GSimpleGA(genome)
ga.evolve(freq_stats=10)
print ga.bestIndividual()
```

## Next steps

- [Extending Pyevolve](extending.md)
- [Genetic Programming Tutorial](gp_tutorial.md)
- [Snippets](snippets.md)

## Footnotes

[^rawscore]: It is important to note that in Pyevolve, we have `raw score` and `fitness score`, the raw score is the return of the evaluation function and the fitness score is the scaled score or the raw score in absence of a scaling scheme.

[^samplegenome]: The term `sample genome` means one genome which provides the main configuration for all individuals.

[^ganote]: This GA uses non-overlapping populations.
