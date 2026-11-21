# The Interactive Mode

Pyevolve introduced the concept of the `Interactive Mode` in
the course of evolution. When you are evolving, and the Interactive Mode
is enabled, you can press the *ESC Key* anytime during the evolution process. By
pressing that key, you will enter the interactive mode, with a normal
python prompt and the `Interaction` module exposed to you as the "it"
module.

::: {.callout-warning}
note that the Interactive Mode for Linux/Mac was disabled in the
0.6 release of Pyevolve. The cause was the platform dependant code.
To use it in Linux/Mac you must set the generation in wich Pyevolve
will enter in the Interactive Mode by using `GSimpleGA.GSimpleGA.setInteractiveGeneration`
method; see the `Interaction` module documentation for more information.
:::

If you want to continue the evolution, just press *CTRL-D* on Linux or *CTRL-Z*
on Windows.

See this session example:

```text
# pyevolve_ex1_simple.py
Gen. 1 (0.20%): Max/Min/Avg Fitness(Raw) [6.18(11.00)/4.42(1.00)/5.15(5.15)]
Gen. 20 (4.00%): Max/Min/Avg Fitness(Raw) [11.70(15.00)/7.24(3.00)/9.75(9.75)]
Gen. 40 (8.00%): Max/Min/Avg Fitness(Raw) [17.99(21.00)/12.00(9.00)/14.99(14.99)]
Loading module pylab (matplotlib)...  done!
Loading module numpy...  done!

## Pyevolve v.0.6 - Interactive Mode ##
Press CTRL-D to quit interactive mode.
>>>
```

As you can see, when you press the *ESC Key*, a python prompt will be shown and
the evolution will be paused.

Now, *what you can do* with this prompt !?

- See all the current population individuals
- Change the individuals
- Plot graphics of the current population
- Data analysis, etc... python is your limit.

::: {.callout-note}
to use graphical plots you will obviously need the Matplotlib, see more information
in the [requirements](intro.md#requirements) section for more information.
:::

## Inspecting the population

This is a session example:

```
## Pyevolve v.0.6 - Interactive Mode ##
Press CTRL-Z to quit interactive mode.
>>> dir()
['__builtins__', 'ga_engine', 'it', 'population', 'pyevolve']
>>>
>>> population
- GPopulation
        Population Size:         80
        Sort Type:               Scaled
        Minimax Type:            Maximize
        Slot [Scale Method] (Count: 1)
                Name: LinearScaling
                Doc:  Linear Scaling scheme

   .. warning :: Linear Scaling is only for positive raw scores



- Statistics
        Minimum raw score                             = 10.00
        Minimum fitness                               = 13.18
        Standard deviation of raw scores              = 2.71
        Maximum fitness                               = 19.92
        Maximum raw score                             = 23.00
        Fitness average                               = 16.60
        Raw scores variance                           = 7.36
        Average of raw scores                         = 16.60

>>> len(population)
80
>>> individual = population[0]
>>> individual
- GenomeBase
        Score:                   23.000000
        Fitness:                 19.920000

        Slot [Evaluator] (Count: 1)
                Name: eval_func
        Slot [Initializator] (Count: 1)
                Name: G1DListInitializatorInteger
                Doc:  Integer initialization function of G1DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.


        Slot [Mutator] (Count: 1)
                Name: G1DListMutatorSwap
                Doc:  The mutator of G1DList, Swap Mutator
        Slot [Crossover] (Count: 1)
                Name: G1DListCrossoverSinglePoint
                Doc:  The crossover of G1DList, Single Point

   .. warning:: You can't use this crossover method for lists with just one element.



- G1DList
        List size:       50
        List:            [0, 5, 6, 7, 2, 0, 8, 6, 0, 0, 8, 7, 5, 6, 6, 0, 0, 3, 0, 4, 0, 0, 9, 0, 9, 2, 0, 0, 4, 2
, 5, 0, 0, 2, 0, 0, 0, 1, 8, 7, 0, 8, 9, 0, 8, 0, 0, 0, 9, 0]
```

## The exposed modules and objects

The `Interaction` module is imported with the name "it", you can see
it's contents by calling the python native *dir()*:

```
>>> dir()
['__builtins__', 'ga_engine', 'it', 'population', 'pyevolve']
```

The namespace has the following modules:

> *ga_engine*
>
> : The `GSimpleGA.GSimpleGA` instance, the GA Engine.
>
> *it*
>
> : The `Interaction` module, with the utilities and graph
>   plotting functions.
>
> *population*
>
> : The current population.
>
> *pyevolve*
>
> : The main namespace, the `pyevolve` module.

**Using the "it" module**

> *Plotting the current population raw scores histogram*
>
> > ```pycon
> > >>> it.plotHistPopScore(population)
> > ```
> >
> > ![](imgs/iteract_histogram.png){fig-align="center"}
>
> *Plotting the current population raw scores distribution*
>
> > ```pycon
> > >>> it.plotPopScore(population)
> > ```
> >
> > ![](imgs/iteract_plotraw.png){fig-align="center"}
>
> *Get all the population raw scores*
>
> > ```pycon
> > >>> popScores = it.getPopScores(population)
> > >>> popScores
> > [17.0, 17.0, 16.0, 15.0, 13.0, 11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0,
> > 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0,
> >  8.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 5.0
> > , 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0]
> > ```
