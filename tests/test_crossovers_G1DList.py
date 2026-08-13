import pytest
from unittest.mock import patch

from pyevolve.representations.G1DList import G1DList

from pyevolve.perturbations.CrossoverG1DList import G1DListCrossoverRealSBX, G1DListCrossoverSinglePoint, G1DListCrossoverTwoPoint, G1DListCrossoverUniform

from .test_crossovers import CrossoverTestCase

class G1DListCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G1DList(3)
        self.mom.genomeList = [1, 2, 3]
        self.dad = G1DList(3)
        self.dad.genomeList = [4, 5, 6]

    @patch('pyevolve.perturbations.CrossoverG1DList.rand_randint')
    def test_single_point(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G1DListCrossoverSinglePoint,
            [1, 5, 6],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G1DListCrossoverSinglePoint,
            [1, 5, 6],
            [4, 2, 3],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.perturbations.CrossoverG1DList.rand_randint')
    def test_two_points(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G1DListCrossoverTwoPoint,
            [1, 2, 3],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G1DListCrossoverTwoPoint,
            [1, 2, 3],
            [4, 5, 6],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform(self, coin_flip_mock):
        coin_flip_mock.return_value = [1, 0, 0]
        self.assertCrossoverResultsEqual(
            G1DListCrossoverUniform,
            [4, 5, 6],
            [1, 2, 3],
        )

    @patch('pyevolve.perturbations.CrossoverG1DList.rand_random')
    def test_crossfill_crossover_sbx(self, rand_mock):
        rand_mock.return_value = 0.6
        self.assertCrossoverResultsEqual(
            G1DListCrossoverRealSBX,
            [0.9696386870268516, 1.9692699516972016, 2.9692611909097177],
            [4.030739398252697, 5.030739398252697, 6.030739398252697],
        )
