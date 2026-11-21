# Snippets

Here are some snippets to help you.

## Using two mutators at same time

> To use two mutators at same time, you simple add one more to the mutator
> function slot, like this:
>
> > ```pycon
> > >>> genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
> > >>> genome.mutator.add(Mutators.G1DListMutatorSwap)
> > ```
>
> The first line will set the `Mutators.G1DListMutatorRealGaussian`, and the second line
> add one more mutator, the `Mutators.G1DListMutatorSwap`.
>
> As you can see, it's very simple and easy, and you will have two mutation
> operators at same time.
>
> If you want just one of these mutators (picked at random) to be executed at
> the mutation process, set the *random apply* parameter of the `FunctionSlot.FunctionSlot`
> class to True
>
> ```
> >>> genome.mutator.setRandomApply(true)
> ```

## Using one allele for all list (chromosome) elements (genes)

> Sometimes you want to use just one allele type for all genes
> on the 1D List or other chromosomes. You simply add one allele type
> and set the *homogeneous* flag to **True**:
>
> > ```pycon
> > >>> setOfAlleles = GAllele.GAlleles(homogeneous=True)
> > >>> lst = [ "1", "two", 0, 777 ]
> > >>> a = GAllele.GAlleleList(lst)
> > >>> setOfAlleles.add(a)
> > ```
>
> Done. Your setOfAlleles is the `GAllele.GAlleles` class instance with
> the *lst* ([ "1", "two", 0, 777 ]) as alleles in all genes.

## Changing the selection method

> To change the default selection method, you must do this:
>
> > ```pycon
> > >>> ga = GSimpleGA.GSimpleGA(genome)
> > >>> ga.selector.set(Selectors.GTournamentSelector)
> > ```
>
> In this example, we change the selection method to the
> `Selectors.GTournamentSelector`, the Tournament Selector.

## Repeating an evolution with a specific seed

> Using a specific seed, you can guarantee that the evolution will be always
> the same, no matter the number of executions you make.
> To initialize the GA Engine with the specific seed, use the *seed* parameter
> when instantiating the `GSimpleGA.GSimpleGA` class:
>
> ```
> ga_engine = GSimpleGA(genome, 123)
> # or
> ga_engine = GSimpleGA(genome, seed=123)
> ```
>
> The value *123* will be passed as the seed to the random function of the GA Engine.

## Writing the evolution statistics to a CSV File

> You can write all the statistics of an evolution to a CSV (Comma Separated Values)
> file using the DB Adapter called `DBAdapters.DBFileCSV`, just create
> an instance of the adapter and attach it to the GA Engine:
>
> ```
> csv_adapter = DBFileCSV(identify="run1", filename="stats.csv")
> ga_engine.setDBAdapter(csv_adapter)
> ```
>
> Now ! Now, when you run your GA, all the stats will be dumped to the CSV file.
> You can set the frequency in which the stats will be dumped, just use the parameter
> *frequency* of the DBFileCSV.

## Use the HTTP Post to dump GA statistics

> With the `DBAdapters.DBURLPost`, you can call an URL with the
> population statistics in every generation or at specific generation
> of the evolution:
>
> ```
> urlpost_adapter = DBURLPost("http://localhost/post.py", identify="run1", frequency=100)
> ga_engine.setDBAdapter(urlpost_adapter)
> ```
>
> Now, the URL "<http://localhost/post.py>" will be called with the statistics params in
> every 100 generations. By default, the adapter will use the HTTP POST method to send
> the parameters, but you can use GET method setting the *post* paramter to *False*.
>
> See the mod:`Statistics` and `DBAdapters.DBURLPost` documentation.

## Using two or more `evaluation function`

> To use two or more `evaluation function`, you can just add all
> the evaluators to the slot:
>
> ```
> genome.evaluator.set(eval_func1)
> genome.evaluator.add(eval_func2)
> ```
>
> The resulting raw score of the genome, when evaluated using more than
> one evaluation function, will be the sum of all returned scores.
>
> **Note:**
> the method *set* of the function slot remove all previous
> functions added to the slot.


## Real-time statistics visualization

> You have three options to view the statistics while in the course
> of the evolution:
>
> **Console statistics**
>
> > You can view the statistics by setting the *freq_stats* parameter
> > of the `GSimpleGA.GSimpleGA.evolve` method. It will dump
> > the statistics in the console.
>
> **Using the sqlite3 DB Adapter**
>
> > You can use the `DBAdapters.DBSQLite` DB Adapter and set
> > the *commit_freq* to a low value, so you can use the Graphical
> > Plotting Tool of Pyevolve to create graphics while evolving.
>
> **Using the VPython DB Adapter**
>
> > Use the `DBAdapters.DBVPythonGraph` DB Adapter, this DB
> > Adapter will show four statistical graphs, it is fast and
> > easy to use.

## How to manually add non-terminal functions to Genetic Programming core {#snippet_gp_explicit}

When you set Pyevolve to automatically catch non-terminal functions for your GP
core you do something like this:

```
ga = GSimpleGA.GSimpleGA(genome)
ga.setParams(gp_terminals       = ['a', 'b'],
             gp_function_prefix = "gp")
```

The "gp_function_prefix" parameter tells Pyevolve to catch any functions starting
with "gp". But there are times that you want to add each function manually, so
you just need to add a dictionary parameter called "gp_function_set", like this:

```
ga.setParams(gp_terminals       = ['a', 'b'],
             gp_function_set = {"gp_add" :2,
                                "gp_sub" :2,
                                "gp_sqrt":1})
```

Note the "gp_function_set" dictionary parameter which holds as key the function
name and for the value, the number of arguments from that function, in this case
we have "gp_add" with 2 parameters, "gp_sub" with 2 and "gp_sqrt" with just one.

## Passing extra parameters to the individual

Sometimes we want to add extra parameters which we need the individuals must
carry, in this case, we can use the method `GenomeBase.GenomeBase.setParams`
to set internal parameters of the individual and the method `GenomeBase.GenomeBase.getParam`
to get it's parameters back, see an example:

```
def evaluation_function(genome):
   parameter_a = genome.getParam("parameter_a")

def main():
   # (...)
   genome = G1DList.G1DList(20)
   genome.setParams(rangemin=-5.2, rangemax=5.30, parameter_a="my_value")
   # (...)
```

::: {.callout-note}
Due to performance issues, Pyevolve doesn't copy the internal parameters
into each new created individual, it simple references the original
parameters, this reduces memory and increases speed.
:::

## Using ephemeral constants in Genetic Programming

You can use an ephemeral constant in Pyevolve GP core by using the "ephemeral:"
prefix in your GP terminals, like in:

```
ga = GSimpleGA.GSimpleGA(genome)
ga.setParams(gp_terminals       = ['a', 'b', 'ephemeral:random.randint(1,10)'],
        gp_function_prefix = "gp")
```

In this example, the ephemeral constant will be an integer value between 1 and 10. You
can use any method of the Python `random` module to specify the ephemeral constant.
