# Examples

All the examples can be downloaded from the [download sec](intro.md#download_sec) section, **they are not**
included in the installation package.

## Example01 Simple

Filename: `examples/pyevolve_ex01_simple.py`

```python

{{< include ../../examples/pyevolve_ex01_simple.py >}}

```

## Example01 Simple Dbadapter

Filename: `examples/pyevolve_ex01_simple_dbadapter.py`

```python

{{< include ../../examples/pyevolve_ex01_simple_dbadapter.py >}}

```

## Example01 Simple Minimize

Filename: `examples/pyevolve_ex01_simple_minimize.py`

```python

{{< include ../../examples/pyevolve_ex01_simple_minimize.py >}}

```

## Example02 Realgenetic Algorithmuss

Filename: `examples/pyevolve_ex02_realgauss.py`

```python

{{< include ../../examples/pyevolve_ex02_realgauss.py >}}

```

## Example03 Schaffer


Minimize the Schaffer F6 function with a real-valued genetic algorithm.

The Schaffer F6 function is a deceptive function, considered a GA-hard function to optimize:

The two-dimensional genome is initialized with real values and evolved using
Gaussian mutation and roulette-wheel selection.

Run this example with ``python examples/pyevolve_ex03_schaffer.py``.

Public functions:
    schafferF6(genome): Evaluate the Schaffer F6 objective for a genome.
    run_main(): Configure and run the genetic algorithm.

Filename: `examples/pyevolve_ex03_schaffer.py`

```python

{{< include ../../examples/pyevolve_ex03_schaffer.py >}}

```

## Example04 Sigmatrunc


This example shows the use of the sigma truncation scale method.
It tries to minimize a function with negative results:

Filename: `examples/pyevolve_ex04_sigmatrunc.py`

```python

{{< include ../../examples/pyevolve_ex04_sigmatrunc.py >}}

```

## Example05 Callback


This example shows the use of the `step callback function`:

Filename: `examples/pyevolve_ex05_callback.py`

```python

{{< include ../../examples/pyevolve_ex05_callback.py >}}

```

## Example06 Dbadapter


This example shows the use of the DB Adapters (`DBAdapters`) :
You can use the DB Adapters to store the evolution data in
    - a database,
    - CSV file.

Filename: `examples/pyevolve_ex06_dbadapter.py`

```python

{{< include ../../examples/pyevolve_ex06_dbadapter.py >}}

```

## Example07 Rastrigin


This example minimizes the deceptive function Rastrigin with 20 variables:

Filename: `examples/pyevolve_ex07_rastrigin.py`

```python

{{< include ../../examples/pyevolve_ex07_rastrigin.py >}}

```

## Example08 Genetic Algorithmuss Int


This example shows the use of the Gaussian Integer Mutator:
(`Mutators.G1DListMutatorIntegerGaussian`):

Filename: `examples/pyevolve_ex08_gauss_int.py`

```python

{{< include ../../examples/pyevolve_ex08_gauss_int.py >}}

```

## Example09 G2Dlist


This example shows the use of the 2D list genome (`G2DList.G2DList`):

Filename: `examples/pyevolve_ex09_g2dlist.py`

```python

{{< include ../../examples/pyevolve_ex09_g2dlist.py >}}

```

## Example10 G1Dbinstr


This example shows the use of the 1D Binary String genome:

Filename: `examples/pyevolve_ex10_g1dbinstr.py`

```python

{{< include ../../examples/pyevolve_ex10_g1dbinstr.py >}}

```

## Example11 Allele

Filename: `examples/pyevolve_ex11_allele.py`

```python

{{< include ../../examples/pyevolve_ex11_allele.py >}}

```

## Example13 Sphere


This is the GA to solve the sphere function:

Filename: `examples/pyevolve_ex13_sphere.py`

```python

{{< include ../../examples/pyevolve_ex13_sphere.py >}}

```

## Example14 Ackley


This example minimizes the Ackley F1 function, a deceptive function:

Filename: `examples/pyevolve_ex14_ackley.py`

```python

{{< include ../../examples/pyevolve_ex14_ackley.py >}}

```

## Example15 Rosenbrock


This example minimizes the Rosenbrock function, another deceptive function:

Filename: `examples/pyevolve_ex15_rosenbrock.py`

```python

{{< include ../../examples/pyevolve_ex15_rosenbrock.py >}}

```

## Example16 G2Dbinstr

Filename: `examples/pyevolve_ex16_g2dbinstr.py`

```python

{{< include ../../examples/pyevolve_ex16_g2dbinstr.py >}}

```

## Example17 Gtree

Filename: `examples/pyevolve_ex17_gtree.py`

```python

{{< include ../../examples/pyevolve_ex17_gtree.py >}}

```

## Example18 Gp

Filename: `examples/pyevolve_ex18_gp.py`

```python

{{< include ../../examples/pyevolve_ex18_gp.py >}}

```

## Example19 Gp

Filename: `examples/pyevolve_ex19_gp.py`

```python

{{< include ../../examples/pyevolve_ex19_gp.py >}}

```

## Example20 Gp Dotwrite

Filename: `examples/pyevolve_ex20_gp_dotwrite.py`

```python

{{< include ../../examples/pyevolve_ex20_gp_dotwrite.py >}}

```

## Example21 Nqueens


This example shows the use of GA to solve the n-queens problem for a
chess board of size 64x64:

Filename: `examples/pyevolve_ex21_nqueens.py`

```python

{{< include ../../examples/pyevolve_ex21_nqueens.py >}}

```

## Example22 Monkey


This example was kindly contributed by Jelle Feringa, it shows the
[Infinite Monkey Theorem](http://en.wikipedia.org/wiki/Infinite_monkey_theorem):

Filename: `examples/pyevolve_ex22_monkey.py`

```python

{{< include ../../examples/pyevolve_ex22_monkey.py >}}

```

## Example23 Initial Population

Filename: `examples/pyevolve_ex23_initial_population.py`

```python

{{< include ../../examples/pyevolve_ex23_initial_population.py >}}

```

## Example24 Real Minimum Putnam B1

Filename: `examples/pyevolve_ex24_real_minimum_Putnam_B1.py`

```python

{{< include ../../examples/pyevolve_ex24_real_minimum_Putnam_B1.py >}}

```

## Example Cvrp Genetic Algorithm Hybrid Selection

Filename: `examples/pyevolve_ex_cvrp_ga_hybrid_selection.py`

```python

{{< include ../../examples/pyevolve_ex_cvrp_ga_hybrid_selection.py >}}

```

## Example Traveling Sales Person 01


The Travelling Salesman Problem (TSP)


This example shows the use of Pyevolve to solve the [TSP](http://en.wikipedia.org/wiki/Traveling_salesman_problem):

This example will plot a file called `tsp_result.png` in the same
current working directory. The generated image will be the best result of the
TSP, it looks like:

> ![](imgs/ex_12_tsp_result.png){fig-align="center"}

To plot this image, you will need the Python Imaging Library (PIL).

::: {.callout-tip}
[Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/)

: The Python Imaging Library (PIL) adds image processing capabilities to your
  Python interpreter. This library supports many file formats, and provides
  powerful image processing and graphics capabilities.
:::

Filename: `examples/pyevolve_ex_tsp_01.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_01.py >}}

```

## Example Traveling Sales Person 02 Selector

Filename: `examples/pyevolve_ex_tsp_02_selector.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_02_selector.py >}}

```

## Example Traveling Sales Person 03 Genetic Algorithm Crossover Greedy

Filename: `examples/pyevolve_ex_tsp_03_ga_crossover_Greedy.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_03_ga_crossover_Greedy.py >}}

```

## Example Traveling Sales Person 03 Genetic Algorithm Crossover Igx

Filename: `examples/pyevolve_ex_tsp_03_ga_crossover_IGX.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_03_ga_crossover_IGX.py >}}

```

## Example Traveling Sales Person 03 Genetic Algorithm Crossover Pmx

Filename: `examples/pyevolve_ex_tsp_03_ga_crossover_PMX.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_03_ga_crossover_PMX.py >}}

```

## Example Traveling Sales Person 04 Selectorexplorationexploitationbalance

Filename: `examples/pyevolve_ex_tsp_04_SelectorExplorationExploitationBalance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_04_SelectorExplorationExploitationBalance.py >}}

```

## Example Traveling Sales Person 05 Genetic Algorithm Crossover Distance

Filename: `examples/pyevolve_ex_tsp_05_ga_crossover_distance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_05_ga_crossover_distance.py >}}

```

## Example Traveling Sales Person 05 Genetic Algorithm Crossover Distance Loop

Filename: `examples/pyevolve_ex_tsp_05_ga_crossover_distance_loop.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_05_ga_crossover_distance_loop.py >}}

```

## Example Traveling Sales Person 06 Genetic Algorithm Hybrid Selection Coordinate

Filename: `examples/pyevolve_ex_tsp_06_ga_hybrid_selection_coordinate.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_06_ga_hybrid_selection_coordinate.py >}}

```

## Example Traveling Sales Person 07 Genetic Algorithm Hybrid Selection Distance

Filename: `examples/pyevolve_ex_tsp_07_ga_hybrid_selection_distance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_07_ga_hybrid_selection_distance.py >}}

```

## Example Traveling Sales Person 08 Genetic Algorithm Hybrid Selection Distance

Filename: `examples/pyevolve_ex_tsp_08_ga_hybrid_selection_distance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_08_ga_hybrid_selection_distance.py >}}

```
