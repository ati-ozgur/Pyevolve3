from pyevolve import Initializators
from pyevolve.representations.G1DBinaryString import G1DBinaryString
from pyevolve.representations.G1DList import G1DList
from pyevolve.representations.G2DList import G2DList
from pyevolve.representations.GTree import GTree


def test_binary_string_initializator():
    genome = G1DBinaryString(3)
    Initializators.G1DBinaryStringInitializator(genome)
    for gen in genome.genomeList:
        assert gen in [0, 1]


def test_1d_list_real_initializator():
    genome = G1DList(3)
    Initializators.G1DListInitializatorReal(genome)
    for gen in genome.genomeList:
        assert type(gen) is float


def test_2d_list_integer_initializator():
    genome = G2DList(3, 3)
    Initializators.G2DListInitializatorInteger(genome)
    for gen_row in genome.genomeList:
        for gen in gen_row:
            assert type(gen) is int


def test_2d_list_real_initializator():
    genome = G2DList(3, 3)
    Initializators.G2DListInitializatorReal(genome)
    for gen_row in genome.genomeList:
        for gen in gen_row:
            assert type(gen) is float


def test_tree_integer_initializator():
    genome = GTree()
    genome.setParams(max_depth=3)
    Initializators.GTreeInitializatorInteger(genome)
    for gen in genome.getAllNodes():
        assert type(gen.getData()) is int
