import pytest
from unittest.mock import patch

from itertools import cycle

from pyevolve.perturbations.CrossoverG2DList import G2DListCrossoverSingleHPoint, G2DListCrossoverSingleVPoint, G2DListCrossoverUniform
from pyevolve.representations.G2DList import G2DList


from .test_crossovers import CrossoverTestCase

class G2DListCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G2DList(3, 3)
        self.mom.genomeList = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.dad = G2DList(3, 3)
        self.dad.genomeList = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform_crossover(self, coin_flip_mock):
        coin_flip_mock.return_value = cycle([1, 0, 0])
        self.assertCrossoverResultsEqual(
            G2DListCrossoverUniform,
            [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        )

    @patch('pyevolve.perturbations.CrossoverG2DList.rand_randint')
    def test_svp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G2DListCrossoverSingleVPoint,
            [[1, 4, 7], [4, 5, 8], [7, 6, 9]],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G2DListCrossoverSingleVPoint,
            [[1, 4, 7], [4, 5, 8], [7, 6, 9]],
            [[1, 2, 3], [2, 5, 6], [3, 8, 9]],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.perturbations.CrossoverG2DList.rand_randint')
    def test_shp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G2DListCrossoverSingleHPoint,
            [[1, 2, 3], [2, 5, 8], [3, 6, 9]],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G2DListCrossoverSingleHPoint,
            [[1, 2, 3], [2, 5, 8], [3, 6, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            crossover_extra_kwargs={'count': 2}
        )
