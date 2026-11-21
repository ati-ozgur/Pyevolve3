# Genetic Programming Tutorial

In the release 0.6 of Pyevolve, the new Genetic Programming core was added to the framework.
In the [pyevolve-example18](examples.md#pyevolve-example18) you'll see how simple and easy the Pyevolve GP core is
when compared with other statically-typed languages.

Here is a simple example:

```
from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
import math

rmse_accum = Util.ErrorAccumulator()

def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return math.sqrt(abs(a))

def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()
   code_comp = chromosome.getCompiledCode()

   for a in xrange(0, 5):
      for b in xrange(0, 5):
         evaluated     = eval(code_comp)
         target        = math.sqrt((a*a)+(b*b))
         rmse_accum   += (target, evaluated)

   return rmse_accum.getRMSE()

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=4, method="ramped")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a', 'b'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(50)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.25)
   ga.setPopulationSize(800)

   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best

if __name__ == "__main__":
   main_run()
```

Let's work now step by step on the code to learn what each building block means. The
first part you see the imports:

```
from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
import math
```

The `Util` module is where we'll find many utilities functions and classes like `Util.ErrorAccumulator`.
The `GTree` is where the `GTree.GTreeGP` class resides, which is the main genome used by the GP core of Pyevolve.
Note that we are importing the `GSimpleGA` module, in fact, the GA core will detect when you use a Genetic Programming
genome and will act as the GP core. The modules `Consts` and `math` imported here are for auxiliary use only.
Next we have:

```
rmse_accum = Util.ErrorAccumulator()
```

Here we instantiate the `Util.ErrorAccumulator`, which is a simple accumulator for errors. It has methods for getting
`Adjusted Fitness`, [Mean Square Error](http://en.wikipedia.org/wiki/Mean_squared_error),
[Root Mean Square Error](http://en.wikipedia.org/wiki/Root_mean_squared_error), mean, squared or non-squared error measures.
In the next block we define some GP operators:

```
def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return math.sqrt(abs(a))
```

Observe that they are simple Python functions starting with the "gp" prefix. This is important if you want
Pyevolve to automatically add them as non-terminals of the GP core. As you can note, the square root is a protected
square root, since it uses the absolute value of "a" (we don't have square root of negative numbers, except in the
complex analysis). You can define any other function you want.
Later we have the declaration of the `Evaluation function` for the GP core:

```
def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()
   code_comp = chromosome.getCompiledCode()

   for a in xrange(0, 5):
      for b in xrange(0, 5):
         evaluated     = eval(code_comp)
         target        = math.sqrt((a*a)+(b*b))
         rmse_accum   += (target, evaluated)

   return rmse_accum.getRMSE()
```

As you see, the `eval_func` receives one parameter, the chromosome (the GP Tree in our case, an instance of the
`GTree.GTreeGP` class). We first declare the global error accumulator and reset it, since we'll start to evaluate
a new individual, a new "program". In the line where we call `GTree.GTreeGP.getCompiledCode()`, here is what
happens: Pyevolve will get the pre-ordered expression of the GP Tree and then will compile it into Python bytecode,
and will return to you an object of the type "code". This object can then be executed using the Python native `eval`
function. Why compile it to bytecode ? Because if we don't compile the program into Python bytecode, we will need
to parse the Tree every time we want to evaluate our program using defined variables, and since this is a commom use
of the GP program, this is the fastest way we can do it in pure Python.

In the next block, we simply iterate using two variables "a" and "b".

::: {.callout-note}
Please note that the variable names here is the same that we will use as terminals later.
:::

What you see now is the evaluation of the "code_comp" (which is the GP individual) and the evaluation of the objective
function in which we want to fit (the Pythagorean theorem). Next we simply add the "target" value we got from the
Pythagorean theorem and the "evaluated" value of the individual to the Error Accumulator.
In the end of the evaluation function, we return the [Root Mean Square Error](http://en.wikipedia.org/wiki/Root_mean_squared_error).
If you don't like to add the evaluated and the target values using a tuple, you can use the `Util.ErrorAccumulator.append`
method, which will give the same results.

Next we start to define our `main_run` function:

```
def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=4, method="ramped")
   genome.evaluator.set(eval_func)
```

The first thing we instantiate here is the `GTree.GTreeGP` class (the GP individual, the Tree). Next
we set some parameters of the GTreeGP. The first is the "max_depth", which is used by genetic operators
and initializators to control bloat; in this case, we use 4, which means that no Tree with a height > 4 will
grow. Next we set the "method", this is the initialization method, and the values accepted here depends of
the initialization method used, since we do not have specified the initialization method, Pyevolve will
use the default, which is the `Initializators.GTreeGPInitializator` (it accepts "grow", "full" and "ramped"
methods for Tree initialization. And in the last line of this block, we set the previously defined evaluation
function called `eval_func`.
In the next block we then instantiate the GSimpleGA core and set some parameters:

```
ga = GSimpleGA.GSimpleGA(genome)
ga.setParams(gp_terminals       = ['a', 'b'],
             gp_function_prefix = "gp")
```

The "ga" object will hold an instance of the `GSimpleGA.GSimpleGA` class, which is the core for both
Genetic Algorithms and Genetic Programming. Pyevolve will automatically detect if you are creating a environment
for a GP or for a GA. Next we set some parameters of the core, the first is a list called "gp_terminals".
The "gp_terminals" will hold the "variables" or in GP vocabulary . Note that the
name of the terminals are the same we used in our evaluation function called `eval_func`. The next step
is to define the prefix of the GP operators (functions) or the `Non-terminal node`. Pyevolve will automatically
search for all functions defined in the module which starts with "gp" (example: gp_sub, gp_add, gp_IHateJava, etc...)
and will add these functions as the non-terminal nodes of the GP core.

The next part of the code is almost the same as used in the Genetic Algorithms applications, they are the EA parameters
to setup and start the evolution:

```
ga.setMinimax(Consts.minimaxType["minimize"])
ga.setGenerations(50)
ga.setCrossoverRate(1.0)
ga.setMutationRate(0.25)
ga.setPopulationSize(800)

ga(freq_stats=10)
best = ga.bestIndividual()
print best
```

And in the last part of the source code, we have:

```
if __name__ == "__main__":
   main_run()
```

This part is important, since Pyevolve needs to know some information about objects in the main module using instrospection.
You **NEED** to declare this check, the `multiprocessing` module of Python only works with this too, so if
you're planning to use it, please do not forget it.

And that's it, you have completed your first GP program.

## Visualizing individuals

Pyevolve comes with a plotting utility to create images of your GP individuals. It uses
"pydot" and "Graphviz" to create those images. For more information, see the [requirements](intro.md#requirements) section.
What you need to change to see, for example, the first 3 best individuals of your first generation is to
add a `Step callback function` into the code. Let's first define the callback function:

```
def step_callback(gp_engine):
    if gp_engine.getCurrentGeneration() == 0:
        GTree.GTreeGP.writePopulationDot(gp_engine, "trees.jpg", start=0, end=3)
```

The code is self-explanatory, the parameter is the GP core, first we check if it is the first generation and
then we use the `GTree.GTreeGP.writePopulationDot` method to write to the "trees.jpg" file, the
range from 0 and 3 individuals of the population. Then in the main function where we instantiate the GP core,
we simply use:

```
ga.stepCallback.set(step_callback)
```

And the result will be:

![](imgs/gp_trees_img1.jpg){fig-align="center"}
