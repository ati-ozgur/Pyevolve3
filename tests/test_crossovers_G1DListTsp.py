import random
import unittest

import pytest
from unittest.mock import patch

from pyevolve.perturbations.CrossoverG1DListTspPermutations import (
    G1DListCrossoverCutCrossfill,
    G1DListCrossoverCycle,
    G1DListCrossoverEdge,
    G1DListCrossoverGreedy,
    G1DListCrossoverIGX,
    G1DListCrossoverMPX,
    G1DListCrossoverOX,
    G1DListCrossoverOX2,
    G1DListCrossoverPMX,
    G1DListCrossoverPOS,
    G1DListCrossoverSequentialConstructive,
)

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

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_greedy_crossover_uses_zero_based_distance_matrix(self, rand_mock):
        class NonNegativeMatrix(list):
            def __getitem__(self, index):
                if index < 0:
                    raise AssertionError("Distance matrix indices must be non-negative")
                return super().__getitem__(index)

        rand_mock.return_value = 0
        self.mom.genomeList = [0, 1, 2]
        self.dad.genomeList = [2, 1, 0]
        self.mom.setParams(
            distance_matrix_list=NonNegativeMatrix(
                NonNegativeMatrix(row) for row in (
                    [0, 1, 2],
                    [1, 0, 3],
                    [2, 3, 0],
                )
            )
        )

        sister, brother = G1DListCrossoverGreedy(
            None,
            mom=self.mom,
            dad=self.dad,
            count=2,
        )

        self.assertEqual(set(sister.genomeList), {0, 1, 2})
        self.assertEqual(set(brother.genomeList), {0, 1, 2})

    def test_sequential_constructive_crossover_without_depot_gene(self):
        self.mom.genomeList = [1, 2, 3]
        self.dad.genomeList = [3, 1, 2]
        self.mom.setParams(
            distance_matrix_list=[
                [0, 1, 2, 3],
                [1, 0, 4, 5],
                [2, 4, 0, 6],
                [3, 5, 6, 0],
            ]
        )

        sister, brother = G1DListCrossoverSequentialConstructive(
            None,
            mom=self.mom,
            dad=self.dad,
            count=2,
        )

        self.assertEqual(set(sister.genomeList), {1, 2, 3})
        self.assertEqual(set(brother.genomeList), {1, 2, 3})


def _tour(cities):
    genome = G1DList(len(cities))
    genome.genomeList = list(cities)
    return genome


class G1DListCrossoversTspMappingTestCase(CrossoverTestCase):
    """Fixed-input results for PMX, OX2, POS and MPX on an 8-city tour.

    The mocked ``rand_randint`` values pick the cut points / positions, so each
    expected child can be checked by hand against the operator's definition.
    """

    def setUp(self):
        self.mom = _tour([0, 1, 2, 3, 4, 5, 6, 7])
        self.dad = _tour([3, 7, 5, 1, 6, 0, 2, 4])

    def assertBothCounts(self, crossover, rand_mock, rand_values, expected_sister, expected_brother):
        rand_mock.side_effect = list(rand_values)
        self.assertCrossoverResultsEqual(crossover, expected_sister, None, crossover_extra_kwargs={'count': 1})
        rand_mock.side_effect = list(rand_values)
        self.assertCrossoverResultsEqual(
            crossover, expected_sister, expected_brother, crossover_extra_kwargs={'count': 2})
        # Parents must not be modified
        self.assertEqual(self.mom.genomeList, [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(self.dad.genomeList, [3, 7, 5, 1, 6, 0, 2, 4])

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_pmx_crossover(self, rand_mock):
        # cut points c1=2, c2=5
        self.assertBothCounts(G1DListCrossoverPMX, rand_mock, [2, 5],
                              [1, 7, 2, 3, 4, 0, 5, 6], [0, 3, 5, 1, 6, 2, 4, 7])

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_ox2_crossover(self, rand_mock):
        # 3 positions: 1, 4, 6
        self.assertBothCounts(G1DListCrossoverOX2, rand_mock, [3, 1, 4, 6],
                              [3, 7, 5, 1, 4, 0, 2, 6], [0, 1, 7, 3, 4, 5, 6, 2])

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_pos_crossover(self, rand_mock):
        # 3 positions: 1, 4, 6
        self.assertBothCounts(G1DListCrossoverPOS, rand_mock, [3, 1, 4, 6],
                              [0, 7, 1, 3, 6, 4, 2, 5], [3, 1, 7, 5, 4, 0, 6, 2])

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_mpx_crossover(self, rand_mock):
        # cut points c1=2, c2=6 -> copied segment is positions 2..5
        self.assertBothCounts(G1DListCrossoverMPX, rand_mock, [2, 6],
                              [2, 3, 4, 5, 7, 1, 6, 0], [5, 1, 6, 0, 2, 3, 4, 7])

    def test_cycle_crossover_alternates_parents_per_cycle(self):
        # Three cycles by position: {0, 3, 6, 7}, {1, 2, 4}, {5}.
        # Sister takes them from mom, dad, mom; brother is the complement (dad, mom, dad).
        # An odd cycle count used to make the brother a copy of the sister.
        self.dad = _tour([7, 4, 1, 0, 2, 5, 3, 6])
        self.assertCrossoverResultsEqual(
            G1DListCrossoverCycle, [0, 4, 1, 3, 2, 5, 6, 7], None, crossover_extra_kwargs={'count': 1})
        self.assertCrossoverResultsEqual(
            G1DListCrossoverCycle, [0, 4, 1, 3, 2, 5, 6, 7], [7, 1, 2, 0, 4, 5, 3, 6],
            crossover_extra_kwargs={'count': 2})
        # Parents must not be modified (count=1 used to leave them swapped)
        self.assertEqual(self.mom.genomeList, [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(self.dad.genomeList, [7, 4, 1, 0, 2, 5, 3, 6])


class G1DListCrossoversTspInvariantsTestCase(unittest.TestCase):
    """Seeded sweep over random tours checking properties every run must satisfy."""

    CROSSOVERS = (G1DListCrossoverPMX, G1DListCrossoverOX2, G1DListCrossoverPOS, G1DListCrossoverMPX,
                  G1DListCrossoverCycle)
    SEEDS = range(200)

    @staticmethod
    def _parents(seed):
        rng = random.Random(seed)
        size = rng.randint(3, 30)
        mom, dad = list(range(size)), list(range(size))
        rng.shuffle(mom)
        rng.shuffle(dad)
        return _tour(mom), _tour(dad)

    def _cross(self, crossover, mom, dad, count, seed):
        random.seed(seed)
        return crossover(None, mom=mom, dad=dad, count=count)

    def test_invariants(self):
        for crossover in self.CROSSOVERS:
            for seed in self.SEEDS:
                with self.subTest(crossover=crossover.__name__, seed=seed):
                    mom, dad = self._parents(seed)
                    mom_list, dad_list = list(mom.genomeList), list(dad.genomeList)

                    sister, brother = self._cross(crossover, mom, dad, 2, seed)
                    only_sister, no_brother = self._cross(crossover, mom, dad, 1, seed)
                    # Same random draws with parents swapped: the sister must be this run's brother
                    swapped_sister, _ = self._cross(crossover, dad, mom, 1, seed)

                    self.assertEqual(sorted(sister.genomeList), sorted(mom_list))
                    self.assertEqual(sorted(brother.genomeList), sorted(mom_list))
                    self.assertIsNone(no_brother)
                    self.assertEqual(only_sister.genomeList, sister.genomeList)
                    self.assertEqual(swapped_sister.genomeList, brother.genomeList)
                    self.assertEqual(mom.genomeList, mom_list)
                    self.assertEqual(dad.genomeList, dad_list)


class G1DListCrossoversTspDistanceInvariantsTestCase(unittest.TestCase):
    """Seeded sweep for the distance-aware Greedy and IGX crossovers."""

    CROSSOVERS = (G1DListCrossoverGreedy, G1DListCrossoverIGX)
    SEEDS = range(100)

    @staticmethod
    def _parents(seed):
        rng = random.Random(seed)
        size = rng.randint(4, 25)
        points = [(rng.random(), rng.random()) for _ in range(size)]
        distances = [[((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 for b in points] for a in points]
        parents = []
        for _ in range(2):
            cities = list(range(size))
            rng.shuffle(cities)
            genome = _tour(cities)
            genome.setParams(distance_matrix_list=distances)
            parents.append(genome)
        return parents

    def test_invariants(self):
        for crossover in self.CROSSOVERS:
            for seed in self.SEEDS:
                with self.subTest(crossover=crossover.__name__, seed=seed):
                    mom, dad = self._parents(seed)
                    mom_list, dad_list = list(mom.genomeList), list(dad.genomeList)

                    random.seed(seed)
                    only_sister, no_brother = crossover(None, mom=mom, dad=dad, count=1)
                    random.seed(seed)
                    sister, brother = crossover(None, mom=mom, dad=dad, count=2)

                    self.assertEqual(sorted(sister.genomeList), sorted(mom_list))
                    self.assertEqual(sorted(brother.genomeList), sorted(mom_list))
                    self.assertIsNone(no_brother)
                    self.assertEqual(only_sister.genomeList, sister.genomeList)
                    # Greedy used to reverse both parents in place when building the brother
                    self.assertEqual(mom.genomeList, mom_list)
                    self.assertEqual(dad.genomeList, dad_list)


class G1DListCrossoverIGXTestCase(unittest.TestCase):
    # Cities on a line: 0 at 0, 1 at 10, 2 at 11, 3 at 30, 4 at 31
    POSITIONS = [0, 10, 11, 30, 31]

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.random.choice')
    def test_first_step_picks_nearest_neighbour_for_both_children(self, choice_mock):
        choice_mock.return_value = 2  # both children start at city 2
        mom = _tour([0, 1, 2, 3, 4])  # neighbours of 2: 1 (distance 1), 3 (19)
        dad = _tour([3, 2, 4, 0, 1])  # neighbours of 2: 3 (19), 4 (20)
        mom.setParams(distance_matrix_list=[[abs(a - b) for b in self.POSITIONS] for a in self.POSITIONS])

        sister, brother = G1DListCrossoverIGX(None, mom=mom, dad=dad, count=2)

        self.assertEqual(sister.genomeList[:2], [2, 1])
        # The brother used to take the farthest neighbour (4) on its first step
        self.assertEqual(brother.genomeList[:2], [2, 1])


class G1DListCrossoverGreedyTestCase(unittest.TestCase):
    # Cities on a line: 0 at 0, 1 at 10, 2 at 11, 3 at 30, 4 at 31
    POSITIONS = [0, 10, 11, 30, 31]

    @patch('pyevolve.perturbations.CrossoverG1DListTspPermutations.rand_randint')
    def test_sister_follows_shorter_parent_edge(self, rand_mock):
        rand_mock.return_value = 0  # sister starts at mom[0] = city 2
        mom = _tour([2, 3, 4, 0, 1])  # mom's edge from 2 goes to 3 (distance 19)
        dad = _tour([4, 2, 1, 0, 3])  # dad's edge from 2 goes to 1 (distance 1)
        mom.setParams(distance_matrix_list=[[abs(a - b) for b in self.POSITIONS] for a in self.POSITIONS])

        sister, brother = G1DListCrossoverGreedy(None, mom=mom, dad=dad, count=2)

        # The sister used to follow the longer edge (2 -> 3)
        self.assertEqual(sister.genomeList[:2], [2, 1])
        self.assertEqual(sorted(brother.genomeList), [0, 1, 2, 3, 4])
