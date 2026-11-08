from pyevolve.initializations.InitializationBinary import G1DBinaryStringInitializator
from pyevolve.initializations.InitializationG1DList import G1DListInitializatorReal
from pyevolve.initializations.InitializationG2DList import G2DListInitializatorInteger, G2DListInitializatorReal
from pyevolve import ConstsTree


from pyevolve.representations.G1DBinaryString import G1DBinaryString
from pyevolve.representations.G1DList import G1DList
from pyevolve.representations.G2DList import G2DList
from pyevolve.representations.GTree import GTree, GTreeGP


def test_binary_string_initializator():
    genome = G1DBinaryString(3)
    G1DBinaryStringInitializator(genome)
    for gen in genome.genomeList:
        assert gen in [0, 1]


def test_1d_list_real_initializator():
    genome = G1DList(3)
    G1DListInitializatorReal(genome)
    for gen in genome.genomeList:
        assert type(gen) is float


def test_2d_list_integer_initializator():
    genome = G2DList(3, 3)
    G2DListInitializatorInteger(genome)
    for gen_row in genome.genomeList:
        for gen in gen_row:
            assert type(gen) is int


def test_2d_list_real_initializator():
    genome = G2DList(3, 3)
    G2DListInitializatorReal(genome)
    for gen_row in genome.genomeList:
        for gen in gen_row:
            assert type(gen) is float


def test_tree_genomes_use_tree_defaults():
    genome = GTree()
    assert genome.initializator[0] is ConstsTree.CDefGTreeInit
    assert genome.mutator[0] is ConstsTree.CDefGGTreeMutator
    assert genome.crossover[0] is ConstsTree.CDefGTreeCrossover

    gp_genome = GTreeGP()
    assert gp_genome.initializator[0] is ConstsTree.CDefGTreeGPInit
    assert gp_genome.mutator[0] is ConstsTree.CDefGGTreeGPMutator
    assert gp_genome.crossover[0] is ConstsTree.CDefGTreeGPCrossover
