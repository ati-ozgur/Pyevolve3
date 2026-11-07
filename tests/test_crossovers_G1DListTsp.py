import pytest
from unittest.mock import patch

from pyevolve.perturbations.CrossoverG1DListTspPermutations import G1DListCrossoverCutCrossfill, G1DListCrossoverEdge, G1DListCrossoverOX

from pyevolve.representations.G1DList import G1DList


from .test_crossovers import CrossoverTestCase

class G1DListCrossoversTspTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G1DList(3)
        self.mom.genomeList = [1, 2, 3]
        self.dad = G1DList(3)
        self.dad.genomeList = [3, 1, 2]

    @pytest.mark.skip(reason='fails because of https://github.com/perone/Pyevolve/issues/26')
    @patch('pyevolve.perturbations.CrossoverG1DList.rand_randint')
    def test_order_crossover(self, rand_mock):
        rand_mock.side_effect = [1, 2]
        self.assertCrossoverResultsEqual(
            G1DListCrossoverOX,
            [1, 2, 3],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G1DListCrossoverOX,
            [1, 2, 3],
            [4, 5, 6],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_crossfill_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G1DListCrossoverCutCrossfill,
            [1, 3, 2],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G1DListCrossoverCutCrossfill,
            [1, 3, 2],
            [3, 1, 2],
            crossover_extra_kwargs={'count': 2}
        )


    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_crossfill_cut_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            G1DListCrossoverCutCrossfill,
            [1, 3, 2],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            G1DListCrossoverCutCrossfill,
            [1, 3, 2],
            [3, 1, 2],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_choice')
    def test_edge_crossover(self, rand_mock):
        rand_mock.side_effect = lambda u: u[0]
        self.assertCrossoverResultsEqual(
            G1DListCrossoverEdge,
            [1, 2, 3],
            [1, 2, 3],
        )
