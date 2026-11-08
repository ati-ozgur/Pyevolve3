"""
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

"""

from helper_tsp import run_tsp

if __name__ == "__main__":
    # run_tsp(problem_name="tsp_random_cities_default"
    #        , crossover_method="SNGL"
    #        , freq_stats=1
    #        )
    run_tsp(problem_name="gr21", crossover_method="PMX", freq_stats=1
            )
