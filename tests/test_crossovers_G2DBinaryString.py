import pytest
from itertools import cycle

from unittest.mock import patch


from pyevolve.perturbations.CrossoverBinary import G2DBinaryStringXSingleHPoint, G2DBinaryStringXSingleVPoint, G2DBinaryStringXUniform
from pyevolve.representations.G2DBinaryString import G2DBinaryString

from .test_crossovers import CrossoverTestCase

class G2DBinaryStringCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G2DBinaryString(3, 3)
        self.mom.genomeString = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
        self.dad = G2DBinaryString(3, 3)
        self.dad.genomeString = [[0, 1, 1], [1, 0, 0], [1, 0, 1]]

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform_crossover(self, coin_flip_mock):
        coin_flip_mock.return_value = cycle([1, 0, 0])
        self.assertCrossoverResultsEqual(
            G2DBinaryStringXUniform,
            [[0, 1, 1], [1, 0, 0], [1, 0, 1]],
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            genome_attr_name='genomeString'
        )

    @patch('pyevolve.perturbations.CrossoverBinary.rand_randint')
    def test_svp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G2DBinaryStringXSingleVPoint,
            [[0, 1, 1], [0, 0, 0], [0, 0, 1]],
            None,
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G2DBinaryStringXSingleVPoint,
            [[0, 1, 1], [0, 0, 0], [0, 0, 1]],
            [[0, 0, 0], [1, 0, 1], [1, 1, 0]],
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.perturbations.CrossoverBinary.rand_randint')
    def test_shp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G2DBinaryStringXSingleHPoint,
            [[0, 0, 0], [1, 0, 0], [1, 0, 1]],
            None,
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G2DBinaryStringXSingleHPoint,
            [[0, 0, 0], [1, 0, 0], [1, 0, 1]],
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 2}
        )


