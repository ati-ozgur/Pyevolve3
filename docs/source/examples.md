# Examples

All the examples can be downloaded from the [download sec](intro.md#download_sec) section, **they are not**
included in the installation package.

## Example 1 - Simple example

Filename: `examples/pyevolve_ex01_simple.py`

This is Example #1, a very simple example:

```python

{{< include ../../examples/pyevolve_ex01_simple.py >}}

```

## Example 2 - Real numbers, Gaussian Mutator

Filename: `examples/pyevolve_ex02_realgauss.py`

This example uses the `Initializators.G1DListInitializatorReal` initializator
and the `Mutators.G1DListMutatorRealGaussian` mutator:

```python

{{< include ../../examples/pyevolve_ex02_realgauss.py >}}

```

## Example 3 - Schaffer F6 deceptive function

Filename: `examples/pyevolve_ex03_schaffer.py`

This examples tries to minimize the Schaffer F6 function. This function is a
deceptive function, considered a GA-hard function to optimize:

```python

{{< include ../../examples/pyevolve_ex03_schaffer.py >}}

```

## Example 4 - Using Sigma truncation scaling

Filename: `examples/pyevolve_ex04_sigmatrunc.py`

This example shows the use of the sigma truncation scale method. It tries
to minimize a function with negative results:

```python

{{< include ../../examples/pyevolve_ex04_sigmatrunc.py >}}

```

## Example 5 - Step callback function

Filename: `examples/pyevolve_ex05_callback.py`

This example shows the use of the `step callback function`:

```python

{{< include ../../examples/pyevolve_ex05_callback.py >}}

```

## Example 6 - The DB Adapters

Filename: `examples/pyevolve_ex06_dbadapter.py`

This example shows the use of the DB Adapters (`DBAdapters`) :

```python

{{< include ../../examples/pyevolve_ex06_dbadapter.py >}}

```

## Example 7 - The Rastrigin function

Filename: `examples/pyevolve_ex07_rastrigin.py`

This example minimizes the deceptive function Rastrigin with 20 variables:

```python

{{< include ../../examples/pyevolve_ex07_rastrigin.py >}}

```

## Example 8 - The Gaussian Integer Mutator

Filename: `examples/pyevolve_ex08_gauss_int.py`

This example shows the use of the Gaussian Integer Mutator:
(`Mutators.G1DListMutatorIntegerGaussian`):

```python

{{< include ../../examples/pyevolve_ex08_gauss_int.py >}}

```

## Example 9 - The 2D List genome

Filename: `examples/pyevolve_ex09_g2dlist.py`

This example shows the use of the 2D list genome (`G2DList.G2DList`):

```python

{{< include ../../examples/pyevolve_ex09_g2dlist.py >}}

```

## Example 10 - The 1D Binary String

Filename: `examples/pyevolve_ex10_g1dbinstr.py`

This example shows the use of the 1D Binary String genome:

```python

{{< include ../../examples/pyevolve_ex10_g1dbinstr.py >}}

```

## Example 11 - The use of alleles

Filename: `examples/pyevolve_ex11_allele.py`

This example shows the use of alleles:

```python

{{< include ../../examples/pyevolve_ex11_allele.py >}}

```

## Example 12 - The Travelling Salesman Problem (TSP)

Filename: `examples/pyevolve_ex_tsp_01.py`

This example shows the use of Pyevolve to solve the [TSP](http://en.wikipedia.org/wiki/Traveling_salesman_problem):

```python

{{< include ../../examples/pyevolve_ex_tsp_01.py >}}

```

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

## Example 13 - The sphere function

Filename: `examples/pyevolve_ex13_sphere.py`

This is the GA to solve the sphere function:

```python

{{< include ../../examples/pyevolve_ex13_sphere.py >}}

```

## Example 14 - The Ackley function

Filename: `examples/pyevolve_ex14_ackley.py`

This example minimizes the Ackley F1 function, a deceptive function:

```python

{{< include ../../examples/pyevolve_ex14_ackley.py >}}

```

## Example 15 - The Rosenbrock function

Filename: `examples/pyevolve_ex15_rosenbrock.py`

This example minimizes the Rosenbrock function, another deceptive function:

```python

{{< include ../../examples/pyevolve_ex15_rosenbrock.py >}}

```

## Example 16 - The 2D Binary String

Filename: `examples/pyevolve_ex16_g2dbinstr.py`

This example shows the use of the 2D Binary String genome:

```python

{{< include ../../examples/pyevolve_ex16_g2dbinstr.py >}}

```

## Example 17 - The Tree genome example

Filename: `examples/pyevolve_ex17_gtree.py`

This example shows the use of the Tree genome:

```python

{{< include ../../examples/pyevolve_ex17_gtree.py >}}

```

## Example 18 - The Genetic Programming example {#pyevolve-example18}

Filename: `examples/pyevolve_ex18_gp.py`

This example shows the use of the GTreeGP genome (for Genetic Programming):

```python

{{< include ../../examples/pyevolve_ex18_gp.py >}}

```

## Example 21 - The n-queens problem (64x64 chess board)

Filename: `examples/pyevolve_ex21_nqueens.py`

This example shows the use of GA to solve the n-queens problem for a
chess board of size 64x64:

```python

{{< include ../../examples/pyevolve_ex21_nqueens.py >}}

```

## Example 22 - The Infinite Monkey Theorem

Filename: `examples/pyevolve_ex22_monkey.py`

This example was kindly contributed by Jelle Feringa, it shows the
[Infinite Monkey Theorem](http://en.wikipedia.org/wiki/Infinite_monkey_theorem):

```python

{{< include ../../examples/pyevolve_ex22_monkey.py >}}

```

## Additional examples

### Simple example with a DB adapter

Filename: `examples/pyevolve_ex01_simple_dbadapter.py`

```python

{{< include ../../examples/pyevolve_ex01_simple_dbadapter.py >}}

```

### Simple example with minimization

Filename: `examples/pyevolve_ex01_simple_minimize.py`

```python

{{< include ../../examples/pyevolve_ex01_simple_minimize.py >}}

```

### Genetic programming example

Filename: `examples/pyevolve_ex19_gp.py`

```python

{{< include ../../examples/pyevolve_ex19_gp.py >}}

```

### Genetic programming example with dot output

Filename: `examples/pyevolve_ex20_gp_dotwrite.py`

```python

{{< include ../../examples/pyevolve_ex20_gp_dotwrite.py >}}

```

### Initial population example

Filename: `examples/pyevolve_ex23_initial_population.py`

```python

{{< include ../../examples/pyevolve_ex23_initial_population.py >}}

```

### Putnam B1 example

Filename: `examples/pyevolve_ex24_real_minimum_Putnam_B1.py`

```python

{{< include ../../examples/pyevolve_ex24_real_minimum_Putnam_B1.py >}}

```

### Hybrid-selection CVRP example

Filename: `examples/pyevolve_ex_cvrp_ga_hybrid_selection.py`

```python

{{< include ../../examples/pyevolve_ex_cvrp_ga_hybrid_selection.py >}}

```

### TSP selector example

Filename: `examples/pyevolve_ex_tsp_02_selector.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_02_selector.py >}}

```

### TSP Greedy crossover example

Filename: `examples/pyevolve_ex_tsp_03_ga_crossover_Greedy.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_03_ga_crossover_Greedy.py >}}

```

### TSP IGX crossover example

Filename: `examples/pyevolve_ex_tsp_03_ga_crossover_IGX.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_03_ga_crossover_IGX.py >}}

```

### TSP PMX crossover example

Filename: `examples/pyevolve_ex_tsp_03_ga_crossover_PMX.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_03_ga_crossover_PMX.py >}}

```

### TSP selector exploration and exploitation example

Filename: `examples/pyevolve_ex_tsp_04_SelectorExplorationExploitationBalance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_04_SelectorExplorationExploitationBalance.py >}}

```

### TSP distance crossover example

Filename: `examples/pyevolve_ex_tsp_05_ga_crossover_distance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_05_ga_crossover_distance.py >}}

```

### TSP distance crossover loop example

Filename: `examples/pyevolve_ex_tsp_05_ga_crossover_distance_loop.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_05_ga_crossover_distance_loop.py >}}

```

### TSP coordinate hybrid-selection example

Filename: `examples/pyevolve_ex_tsp_06_ga_hybrid_selection_coordinate.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_06_ga_hybrid_selection_coordinate.py >}}

```

### TSP distance hybrid-selection example

Filename: `examples/pyevolve_ex_tsp_07_ga_hybrid_selection_distance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_07_ga_hybrid_selection_distance.py >}}

```

### TSP hybrid-selection distance example

Filename: `examples/pyevolve_ex_tsp_08_ga_hybrid_selection_distance.py`

```python

{{< include ../../examples/pyevolve_ex_tsp_08_ga_hybrid_selection_distance.py >}}

```