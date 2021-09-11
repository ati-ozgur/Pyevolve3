from random import choice as rand_choice
import inspect

from ..FunctionSlot import FunctionSlot
from .. import Util

from . import GenomeBase
from . import GTreeNodeBase



class GTreeBase(GenomeBase):
    """ GTreeBase Class - The base class for the tree genomes

    This chromosome class extends the :class:`GenomeBase` classes.

    :param root_node: the root node of the tree

    .. versionadded:: 0.6
       Added the *GTreeBase* class
    """
    __slots__ = ["root_node", "tree_height", "nodes_list", "nodes_leaf", "nodes_branch"]

    def __init__(self, root_node):
        super(GTreeBase, self).__init__()
        self.root_node = root_node
        self.tree_height = None
        self.nodes_list = None

    def processNodes(self, cloning=False):
        """ Creates a *cache* on the tree, this method must be called
        every time you change the shape of the tree. It updates the
        internal nodes list and the internal nodes properties such as
        depth and height.
        """
        if self.root_node is None:
            return
        self.nodes_list = self.getAllNodes()
        self.nodes_leaf = [n for n in self.nodes_list if n.isLeaf()]
        self.nodes_branch = [n for n in self.nodes_list if n.isLeaf() is False]

        if not cloning:
            self.tree_height = self.getNodeHeight(self.getRoot())

    def getRoot(self):
        """ Return the tree root node

        :rtype: the tree root node
        """
        return self.root_node

    def setRoot(self, root):
        """ Sets the root of the tree

        :param root: the tree root node
        """
        if not isinstance(root, GTreeNodeBase):
            Util.raiseException("The root must be a node", TypeError)
        self.root_node = root

    def getNodeDepth(self, node):
        """ Returns the depth of a node

        :rtype: the depth of the node, the depth of root node is 0
        """
        if node == self.getRoot():
            return 0
        else:
            return 1 + self.getNodeDepth(node.getParent())

    def getNodeHeight(self, node):
        """ Returns the height of a node

        .. note:: If the node has no childs, the height will be 0.

        :rtype: the height of the node
        """
        height = 0
        if len(node) <= 0:
            return 0
        for child in node.getChilds():
            h_inner = self.getNodeHeight(child) + 1
            if h_inner > height:
                height = h_inner
        return height

    def getHeight(self):
        """ Return the tree height

        :rtype: the tree height
        """
        return self.tree_height

    def getNodesCount(self, start_node=None):
        """ Return the number of the nodes on the tree
        starting at the *start_node*, if *start_node* is None,
        then the method will count all the tree nodes.

        :rtype: the number of nodes
        """
        count = 1
        if start_node is None:
            start_node = self.getRoot()
        for i in start_node.getChilds():
            count += self.getNodesCount(i)
        return count

    def getTraversalString(self, start_node=None, spc=0):
        """ Returns a tree-formated string of the tree. This
        method is used by the __repr__ method of the tree

        :rtype: a string representing the tree
        """
        str_buff = ""
        if start_node is None:
            start_node = self.getRoot()
            str_buff += "%s\n" % start_node
        spaces = spc + 2
        for child_node in start_node.getChilds():
            str_buff += "%s%s\n" % (" " * spaces, child_node)
            str_buff += self.getTraversalString(child_node, spaces)
        return str_buff

    def traversal(self, callback, start_node=None):
        """ Traversal the tree, this method will call the
        user-defined callback function for each node on the tree

        :param callback: a function
        :param start_node: the start node to begin the traversal
        """
        if not inspect.isfunction(callback):
            Util.raiseException("The callback for the tree traversal must be a function", TypeError)

        if start_node is None:
            start_node = self.getRoot()
            callback(start_node)
        for child_node in start_node.getChilds():
            callback(child_node)
            self.traversal(callback, child_node)

    def getRandomNode(self, node_type=0):
        """ Returns a random node from the Tree

        :param node_type: 0 = Any, 1 = Leaf, 2 = Branch
        :rtype: random node
        """
        lists = (self.nodes_list, self.nodes_leaf, self.nodes_branch)
        cho = lists[node_type]
        if len(cho) <= 0:
            return None
        return rand_choice(cho)

    def getAllNodes(self):
        """ Return a new list with all nodes

        :rtype: the list with all nodes
        """
        node_stack = []
        all_nodes = []
        tmp = None

        node_stack.append(self.getRoot())
        while len(node_stack) > 0:
            tmp = node_stack.pop()
            all_nodes.append(tmp)
            childs = tmp.getChilds()
            node_stack.extend(childs)

        return all_nodes

    def __repr__(self):
        str_buff = "- GTree\n"
        str_buff += "\tHeight:\t\t\t%d\n" % self.getHeight()
        str_buff += "\tNodes:\t\t\t%d\n" % self.getNodesCount()
        str_buff += "\n" + self.getTraversalString()

        return str_buff

    def __len__(self):
        return len(self.nodes_list)

    def __getitem__(self, index):
        return self.nodes_list[index]

    def __iter__(self):
        return iter(self.nodes_list)

    def copy(self, g, node=None, node_parent=None):
        """ Copy the current contents GTreeBase to 'g'

        :param g: the destination GTreeBase tree

        .. note:: If you are planning to create a new chromosome representation, you
                  **must** implement this method on your class.
        """
        if node is None:
            g.tree_height = self.tree_height
            node = self.root_node

        if node is None:
            return None

        newnode = node.clone()

        if node_parent is None:
            g.setRoot(newnode)
        else:
            newnode.setParent(node_parent)
            node_parent.replaceChild(node, newnode)

        for ci in range(len(newnode)):
            GTreeBase.copy(self, g, newnode.getChild(ci), newnode)

        return newnode

    def clone(self):
        """ Clone this GenomeBase

        :rtype: the clone genome

        .. note:: If you are planning to create a new chromosome representation, you
                  **must** implement this method on your class.
        """
        newcopy = GTreeBase(None)
        self.copy(newcopy)
        newcopy.processNodes()
        return newcopy
