import pytest
from unittest.mock import patch

from pyevolve.representations.G1DBinaryString import G1DBinaryString

from pyevolve.perturbations.CrossoverBinary import G1DBinaryStringXSinglePoint, G1DBinaryStringXTwoPoint, G1DBinaryStringXUniform

from .test_crossovers import CrossoverTestCase

class G1DBinaryStringCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G1DBinaryString(3)
        self.mom.append(1)
        self.mom.append(0)
        self.mom.append(0)
        self.dad = G1DBinaryString(3)
        self.dad.append(0)
        self.dad.append(0)
        self.dad.append(1)

    @patch('pyevolve.perturbations.CrossoverBinary.rand_randint')
    def test_single_point(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G1DBinaryStringXSinglePoint,
            [1, 0, 1],
            [0, 0, 0],
            crossover_extra_kwargs={'count': 2}
        )

        self.assertCrossoverResultsEqual(
            G1DBinaryStringXSinglePoint,
            [1, 0, 1],
            None,
            crossover_extra_kwargs={'count': 1}
        )

    @patch('pyevolve.perturbations.CrossoverBinary.rand_randint')
    def test_two_point(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G1DBinaryStringXTwoPoint,
            [1, 0, 0],
            [0, 0, 1],
            crossover_extra_kwargs={'count': 2}
        )

        self.assertCrossoverResultsEqual(
            G1DBinaryStringXTwoPoint,
            [1, 0, 0],
            None,
            crossover_extra_kwargs={'count': 1}
        )

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform(self, coin_flip_mock):
        coin_flip_mock.return_value = [1, 1, 0]
        self.assertCrossoverResultsEqual(
            G1DBinaryStringXUniform,
            [0, 0, 1],
            [1, 0, 0],
        )
