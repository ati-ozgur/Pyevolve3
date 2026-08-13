

from itertools import cycle
import unittest
from unittest.mock import patch

import pytest

from pyevolve.representations.G1DList import G1DList
from pyevolve.representations.G2DBinaryString import G2DBinaryString
from pyevolve.representations.G2DList import G2DList
from pyevolve.representations.GTree import GTree, GTreeNode




class CrossoverTestCase(unittest.TestCase):
    def assertCrossoverResultsEqual(
            self,
            crossover,
            expected_sister,
            expected_brother,
            crossover_extra_kwargs=None,
            genome_attr_name='genomeList',  # TODO refactor with Genome getter method
            assertion_name='assertEqual'
    ):
        def genome_value_getter(g):
            if genome_attr_name:
                return getattr(g, genome_attr_name)
            else:
                return g
        crossover_extra_kwargs = crossover_extra_kwargs or {}
        kwargs = {
            'mom': self.mom,
            'dad': self.dad,
        }
        kwargs.update(crossover_extra_kwargs)
        actual_sister, actual_brother = [genome_value_getter(g) if g else None for g in crossover(None, **kwargs)]
        getattr(self, assertion_name)(actual_sister, expected_sister)
        getattr(self, assertion_name)(actual_brother, expected_brother)







