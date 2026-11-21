# Extending Pyevolve

## Creating the representation

The first thing you must do is to view the source code of the `GenomeBase.GenomeBase` class
or the source of the `G1DBinaryString.G1DBinaryString` class; they are very
simple to understand.

These are the steps to extend Pyevolve with a new representation:

> 1. Create the chromosome representation class
>
> 2. Create the initializator for your chromosome
>
> 3. Create the genetic operators
>
>    4. Create the Mutator
>    5. Create the Crossover

Well, let's begin with the creation of the elegant **1D Binary String** chromosome. This
chromosome is nothing more than a simple array of '0's or '1's, like so: *"001001000"*.

::: {.callout-note}
This 1D Binary String chromosome is an Pyevolve existing chromosome, of course, in the
Pyevolve implementation we have more features that we will implement here in this simple
example.
:::

All of our new chromosomes **must** extend the base class called `GenomeBase.GenomeBase`,
this class contains the basic slots for the genetic operators and all the internal stuff that
you don't need to care about.

Let's code the initial draft of our chromosome class:

```
from GenomeBase import GenomeBase

class G1DBinaryString(GenomeBase):
   pass
```

As you can see, we have imported the `GenomeBase.GenomeBase` class from the `GenomeBase`
module and we have created the *G1DBinaryString* class extending the base class.

The next step is to create our constructor method for our class. I'll show it first and explain later:

```
def __init__(self, length=10):
   GenomeBase.__init__(self)
   self.genomeString = []
   self.stringLength = length
   self.initializator.set(Consts.CDefG1DBinaryStringInit)
   self.mutator.set(Consts.CDefG1DBinaryStringMutator)
   self.crossover.set(Consts.CDefG1DBinaryStringCrossover)
```

Well, we start by calling the base class constructor and then creating an internal list to hold
our '0's and '1's. It is important to note that we don't initialize the list, this will be done
by our initializator function, and it is because of this that we must keep as an internal attribute
the length of your 1D Binary String.

Next, we set our initializator, mutator and crossover to constants. These constants have just
the functions of our genetic operators, but if you want, you can set them later. In this example,
we will use the defaults for the G1D Binary String.

::: {.callout-note}
The attributes self.initializator, self.mutator and self.crossover are all inherited
from the GenomeBase class. They are all function slots (`FunctionSlot.FunctionSlot`).
:::

Now, you *must* provide the **copy()** and **clone()** methods for your chromosome, because they
are used to replicate the chromosome over the population or when needed by some genetic operators
such as reproduction.

The *copy()* method is very simple. What you need to do is to create a method that copy the
contents of your chromosome to another chromosome of the G1DBinaryString class.

Here is our *copy()* method:

```
def copy(self, g):
   """ Copy genome to 'g' """
   GenomeBase.copy(self, g)
   g.stringLength = self.stringLength
   g.genomeString = self.genomeString[:]
```

As you can see, we first call the base class *copy()* method and later we copy
our string length attribute and our internal *genomeString*, which is our list
of '0's and '1's.

::: {.callout-warning}
It is very important to note that you must **COPY** and not just create
a reference to the object. On the line that we have the *self.genomeString[:]*,
if you use just *self.genomeString*, you will create a **REFERENCE** to this
object and not a copy. This a simple warning, but can avoid many headaches.
:::

The next step is to create our *clone()* method. The clone method, as the name says, is a
method which return another instance of the current chromosome with the same contents.

Let's code it:

```
def clone(self):
   """ Return a new instace copy of the genome """
   newcopy = G1DBinaryString(self.stringLength)
   self.copy(newcopy)
   return newcopy
```

We simply create a new instance and use the *copy()* method that we have created to copy
the instance contents.

Ready ! We have our first representation chromosome. You can add many more features by
implementing python operators such as *\_\_getitem\_\_*, *\_\_setitem\_\_*.

## Creating the initializator

Sorry, not written yet.

## Creating the mutator

Sorry, not written yet.

## Creating the crossover

The file Crossovers.py implements the crossover methods available in
Pyevolve. So, that is where you should look to implement your new
crossover method. The process of adding a new crossover method is as
follows:

1. Create a new method such that the name reflects the type of chromosome
   representation it works with, and the crossover method name. For example,
   `Crossovers.G1DListCrossoverRealSBX`, can work with 1D List representations
   and it operates on real values and it is the SBX crossover operator.
2. The method must accept two parameters, 'genome' and 'args'.
3. From 'args', get the two parents which will take part in the crossover,
   gMom and gDad.
4. Once you have gMom and gDad, use them to create the two children, sister
   and brother.
5. Simply return the sister and brother.

Any constants that your crossover method uses should be defined in Consts.py (`Consts`).
