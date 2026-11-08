# What's new ? {#whatsnew}

What's new on the release 0.7:

**Optimizations and bug-fixes**

> Added many general optimizations and bug-fixes. The code is more *pythonic* and stable
> now.

**Documentation, documentation and documentation**

> Added documentation about the new GP core, new features, changes were done
> to reflect API changes here and there, etc...

**Function Slots - Functions now have weights**

> Added a new `weight` parameter to the `add` method of the
> `FunctionSlot.FunctionSlot` class. This parameter is
> used when you enable the *random apply* of the slot. See
> the class for more information.

**Scaling Scheme - the Boltzmann scaling**

> Added the Boltzmann scaling scheme, this scheme uses a temperature which is reduced
> each generation by a small amount. As the temperature decreases, the difference
> spread between the high and low fitnesses increases. See the description
> on the `Scaling.BoltzmannScaling` function.

**Scaling Scheme - Exponential and Saturated scaling**

> Added the Exponential and Saturated scaling schemes, using the exponential function
> to calculate the fitness values. See more in `Scaling.ExponentialScaling` and
> `Scaling.SaturatedScaling`.

**Selectors - the alternative Tournament Selection**

> Added an alternative Tournament selection method, the `Selectors.GTournamentAlternative`.
> This new Tournament Selector **don't uses** the Roulette Wheel method to pick individuals.

**Statistics - two new statistical measures**

> Added the **fitTot** and the **rawTot** parameters to the `Statistics.Statistics`
> class. See the class documentation for more information.

**Elitism - replacement option**

> Added the method `GSimpleGA.GSimpleGA.setElitismReplacement`. This method is used to set
> the number of individuals cloned on the elitism.

**String representation - resumeString**

> Added the method *resumeString* to all native chromosomes. This method returns a
> small as possible string representation of the chromosome.

**DB Adapter - XML RPC**

> Added a new DB Adapter to send Pyevolve statistics, the XML RPC, to see more information,
> access the docs of the `DBAdapters.DBXMLRPC`.

**DB Adapters - OO redesigned**

> The DB Adapters were redesigned and now there is a super class for all DB Adapters, you
> can create your own DB Adapters subclassing the `DBAdapters.DBBaseAdapter` class.

**The Network module - lan/wan networking**

> Added the `Network` module, this module is used to keep all the
> networking related classes, currently it contains the threaded UDP client/server.

**The Migration module - distributed GA**

> Added the `Migration` module, this module is used to control the
> migration of the distributed GA.

**The G2DBinaryString module - the 2D Binary String**

> Added the `G2DBinaryString` module. This module contains
> the 2D Binary String chromosome representation.

**1D chromosomes - new base class**

> All the 1D choromsomes representation is now extending the
> `GenomeBase.G1DBase` base class.

**Tree chromosome - new Tree representation chromosome**

> Added the module `GTree`, this module contains the
> new `GTree.GTree` chromosome representation and all tree related
> functions and the `GTree.GTreeGP` chromosome used by Genetic Programming.

**VPython DB Adapter - real-time graph statistics**

> Added the new `DBAdapters.DBVPythonGraph` class, this DB
> Adapter uses the VPython to create real-time statistics graphs.

**MySQL DB Adapter - dump statistics to MySQL**

> Added the new `DBAdapters.DBMySQLAdapter` class, this DB Adapter
> will dump statistics to a local or remote MySQL database.

**Genetic Programming - Pyevolve now supports GP**

> Added new support for the Genetic Programming, you can check the
> examples with symbolic regression. The GTreeGP choromsome representation
> is used for the GP main tree.

**Interactive mode - no more platform independent code**

> Code that was platform independent from the Interactive Mode was removed,
> so if you are unable to enter in the Interactive Mode using the ESC key,
> try using the method call to enter in the mode at a defined generation.

**Mutators**

> Added the Simple Inversion Mutation (`Mutators.G1DListMutatorSIM`) for G1DList genome.
>
> Added the Integer Range Mutation (`Mutators.G2DListMutatorIntegerRange`) for the G2DList genome.
>
> Added the Binary String Swap Mutator (`Mutators.G2DListMutatorIntegerRange`) for the G2DBinaryString genome.
>
> Added the Binary String Flip Mutator (`Mutators.G2DBinaryStringMutatorFlip`) for the G2DBinaryString genome.
>
> Added the GTree Swap Mutator (`Mutators.GTreeMutatorSwap`) for the GTree genome.
>
> Added the GTree Integer Range Mutator (`Mutators.GTreeMutatorIntegerRange`) for the GTree genome.
>
> Added the GTree Integer Gaussian Mutator (`Mutators.GTreeMutatorIntegerGaussian`) for the GTree genome.
>
> Added the GTree Real Range Mutator (`Mutators.GTreeMutatorRealRange`) for the GTree genome.
>
> Added the GTree Real Gaussian Mutator (`Mutators.GTreeMutatorRealGaussian`) for the GTree genome.
>
> Added the GTreeGP Operation Mutator (`Mutators.GTreeGPMutatorOperation`) for the GTreeGP genome.
>
> Added the GTreeGP Subtree Mutator (`Mutators.GTreeGPMutatorSubtree`) for the GTreeGP genome.

**Crossovers**

> Added the Cut and Crossfill Crossover (`Crossovers.G1DListCrossoverCutCrossfill`), used for permutations, for
> the G1DList genome.
>
> Added the Uniform Crossover (`Crossovers.G2DBinaryStringXUniform`) for the G2DBinaryString genome.
>
> Added the Single Vert. Point Crossover (`Crossovers.G2DBinaryStringXSingleVPoint`) for the G2DBinaryString genome.
>
> Added the Single Horiz. Point Crossover (`Crossovers.G2DBinaryStringXSingleHPoint`) for the G2DBinaryString genome.
>
> Added the Single Point Crossover (`Crossovers.GTreeCrossoverSinglePoint`) for the GTree genome.
>
> Added the Single Point Strict Crossover (`Crossovers.GTreeCrossoverSinglePointStrict`) for the GTree genome.
>
> Added the Single Point Crossover (`Crossovers.GTreeGPCrossoverSinglePoint`) for the GTreeGP genome.
>
> Added the SBX Crossover (`Crossovers.G1DListCrossoverRealSBX`) for G1DList genome, thanks to Amit Saha.
>
> Added the Edge Recombination (`Crossovers.G1DListCrossoverEdge`) for G1DList genome.

**Initializators**

> Added the Integer Initializator (`Initializators.G2DBinaryStringInitializator`) for the G2DBinaryString genome.
>
> Added the Integer Initializator (`Initializators.GTreeInitializatorInteger`) for the GTree genome.
>
> Added the Allele Initializator (`Initializators.GTreeInitializatorAllele`) for the GTree genome.
>
> Added the GTreeGP (Genetic Programming genome) Initializator (`Initializators.GTreeGPInitializator`).
> It accept the methods: grow, full and ramped.