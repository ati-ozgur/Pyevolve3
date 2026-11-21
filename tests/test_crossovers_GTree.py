from unittest.mock import patch
import unittest

from pyevolve import Consts
from pyevolve.perturbations.CrossoverTree import GTreeCrossoverSinglePointStrict, GTreeGPCrossoverSinglePoint
from pyevolve.representations.GTree import GTree, GTreeGP, GTreeNode, GTreeNodeGP
from pyevolve.representations.GTreeBase import GTreeBase

TERMINAL = Consts.nodeType["TERMINAL"]
NONTERMINAL = Consts.nodeType["NONTERMINAL"]


def _build(spec, make_node, parent=None):
    """Build nodes from ``(data, [children...])``; a bare value is a leaf."""
    data, children = spec if isinstance(spec, tuple) else (spec, [])
    node = make_node(data, bool(children))
    node.setParent(parent)
    for child_spec in children:
        node.addChild(_build(child_spec, make_node, node))
    return node


def _shape(node):
    """Inverse of ``_build``: the tree as nested ``(data, [children...])`` tuples."""
    children = node.getChilds()
    if not children:
        return node.getData()
    return (node.getData(), [_shape(c) for c in children])


def _tree(spec):
    tree = GTree(_build(spec, lambda data, _: GTreeNode(data)))
    tree.processNodes()
    return tree


def _gp_tree(spec):
    tree = GTreeGP(_build(spec, lambda data, branch: GTreeNodeGP(data, NONTERMINAL if branch else TERMINAL)))
    tree.processNodes()
    return tree


def _pick_nodes(*labels):
    """Fake ``getRandomNode``: return the node of this tree whose data is one of ``labels``.

    Crossovers clone the parents first, so nodes are found by label in whichever tree is asked.
    """
    def get_random_node(tree, node_type=0):
        matches = [n for n in tree.getAllNodes() if n.getData() in labels]
        assert len(matches) == 1, f"expected one node labelled {labels} in tree"
        return matches[0]
    return get_random_node


class TreeCrossoverTestMixin:
    crossover = None

    def assertCrossover(self, picks, expected_sister, expected_brother):
        mom_shape, dad_shape = _shape(self.mom.getRoot()), _shape(self.dad.getRoot())
        with patch.object(GTreeBase, "getRandomNode", autospec=True, side_effect=_pick_nodes(*picks)):
            sister, no_brother = type(self).crossover(None, mom=self.mom, dad=self.dad, count=1)
            self.assertEqual(_shape(sister.getRoot()), expected_sister)
            self.assertIsNone(no_brother)

            sister, brother = type(self).crossover(None, mom=self.mom, dad=self.dad, count=2)
            self.assertEqual(_shape(sister.getRoot()), expected_sister)
            self.assertEqual(_shape(brother.getRoot()), expected_brother)

        # Parents are cloned, never modified
        self.assertEqual(_shape(self.mom.getRoot()), mom_shape)
        self.assertEqual(_shape(self.dad.getRoot()), dad_shape)
        return sister, brother


class GTreeCrossoverSinglePointStrictTestCase(TreeCrossoverTestMixin, unittest.TestCase):
    crossover = GTreeCrossoverSinglePointStrict

    def setUp(self):
        self.mom = _tree(("A", ["B", ("C", ["D"])]))
        self.dad = _tree(("X", ["Y", "Z"]))
        for parent in (self.mom, self.dad):
            parent.setParams(max_depth=3)

    def test_swaps_inner_subtrees(self):
        sister, brother = self.assertCrossover(
            ("C", "Y"),
            ("A", ["B", "Y"]),
            ("X", [("C", ["D"]), "Z"]),
        )
        self.assertEqual(sister.getHeight(), 1)
        self.assertEqual(brother.getHeight(), 2)

    def test_mom_root_becomes_dad_subtree(self):
        # nodeMom is the root, so the sister is just dad's subtree
        self.assertCrossover(
            ("A", "Y"),
            "Y",
            ("X", [("A", ["B", ("C", ["D"])]), "Z"]),
        )

    def test_dad_root_becomes_mom_subtree(self):
        self.assertCrossover(
            ("C", "X"),
            ("A", ["B", ("X", ["Y", "Z"])]),
            ("C", ["D"]),
        )

    def test_returns_parent_clones_when_depth_limit_never_met(self):
        # Putting A (height 2) below Y (depth 1) needs max_depth >= 3
        for parent in (self.mom, self.dad):
            parent.setParams(max_depth=2, max_attempt=3)
        with patch.object(GTreeBase, "getRandomNode", autospec=True, side_effect=_pick_nodes("A", "Y")):
            sister, brother = GTreeCrossoverSinglePointStrict(None, mom=self.mom, dad=self.dad, count=2)
        self.assertEqual(_shape(sister.getRoot()), _shape(self.mom.getRoot()))
        self.assertEqual(_shape(brother.getRoot()), _shape(self.dad.getRoot()))


class GTreeGPCrossoverSinglePointTestCase(TreeCrossoverTestMixin, unittest.TestCase):
    crossover = GTreeGPCrossoverSinglePoint

    def setUp(self):
        self.mom = _gp_tree(("add", ["x", ("neg", ["y"])]))
        self.dad = _gp_tree(("mul", ["z", "w"]))
        for parent in (self.mom, self.dad):
            parent.setParams(max_depth=3)

    def test_swaps_terminals(self):
        self.assertCrossover(
            ("y", "z"),
            ("add", ["x", ("neg", ["z"])]),
            ("mul", ["y", "w"]),
        )

    def test_dad_root_replaces_mom_function_node(self):
        self.assertCrossover(
            ("neg", "mul"),
            ("add", ["x", ("mul", ["z", "w"])]),
            ("neg", ["y"]),
        )


if __name__ == "__main__":
    unittest.main()
