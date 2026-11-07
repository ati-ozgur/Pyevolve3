
from .initializations import InitializationTree as Initializators
from .perturbations import CrossoverTree as Crossovers
from .perturbations import MutatorTree as Mutators
from .representations.GTree import GTreeGP


# - GTree defaults
CDefGTreeInit = Initializators.GTreeInitializatorInteger
CDefGGTreeMutator = Mutators.GTreeMutatorIntegerRange
CDefGTreeCrossover = Crossovers.GTreeCrossoverSinglePointStrict

# - GTreeGP defaults
CDefGTreeGPInit = Initializators.GTreeGPInitializator
CDefGGTreeGPMutator = Mutators.GTreeGPMutatorSubtree
CDefGTreeGPCrossover = Crossovers.GTreeGPCrossoverSinglePoint


CDefGPGenomes = [GTreeGP]
