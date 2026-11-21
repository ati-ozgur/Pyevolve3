from unittest.mock import patch

from pyevolve.perturbations.CrossoverG1DListTspPermutations2 import G1DListCrossoverOX6
from pyevolve.representations.G1DList import G1DList

from .test_crossovers import CrossoverTestCase


class G1DListCrossoverOX6TestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G1DList(6)
        self.mom.genomeList = [1, 2, 3, 4, 5, 6]
        self.dad = G1DList(6)
        self.dad.genomeList = [3, 6, 1, 5, 2, 4]

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations2.rand_randint')
    def test_ox6_one_child(self, rand_mock):
        rand_mock.side_effect = [1, 4]
        self.assertCrossoverResultsEqual(
            G1DListCrossoverOX6,
            [6, 2, 3, 4, 1, 5],
            None,
            crossover_extra_kwargs={'count': 1}
        )

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations2.rand_randint')
    def test_ox6_two_children(self, rand_mock):
        rand_mock.side_effect = [1, 4]
        self.assertCrossoverResultsEqual(
            G1DListCrossoverOX6,
            [6, 2, 3, 4, 1, 5],
            [2, 6, 1, 5, 3, 4],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations2.rand_randint')
    def test_ox6_equal_cut_points_redrawn_and_swapped(self, rand_mock):
        # c1 == c2 forces a redraw of c2; c1 > c2 is then swapped to (1, 4)
        rand_mock.side_effect = [4, 4, 1]
        self.assertCrossoverResultsEqual(
            G1DListCrossoverOX6,
            [6, 2, 3, 4, 1, 5],
            [2, 6, 1, 5, 3, 4],
            crossover_extra_kwargs={'count': 2}
        )

    def test_ox6_children_are_valid_tours(self):
        for _ in range(50):
            sister, brother = G1DListCrossoverOX6(None, mom=self.mom, dad=self.dad, count=2)
            self.assertEqual(sorted(sister.genomeList), [1, 2, 3, 4, 5, 6])
            self.assertEqual(sorted(brother.genomeList), [1, 2, 3, 4, 5, 6])
            self.assertIsNot(brother, self.dad)
