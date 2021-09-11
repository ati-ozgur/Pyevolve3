from random import choice as rand_choice
import inspect

from ..FunctionSlot import FunctionSlot
from .. import Util


class GTreeNodeBase(object):
    """ GTreeNodeBase Class - The base class for the node tree genomes

    :param parent: the parent node of the node
    :param childs: the childs of the node, must be a list of nodes

    .. versionadded:: 0.6
       Added the *GTreeNodeBase* class
    """
    __slots__ = ["parent", "childs"]

    def __init__(self, parent, childs=None):
        self.parent = parent
        self.childs = []

        if childs is not None:
            if type(childs) != list:
                Util.raiseException("Childs must be a list of nodes", TypeError)
            typecheck_list = [x for x in childs if not isinstance(x, GTreeNodeBase)]
            if len(typecheck_list) > 0:
                Util.raiseException("Childs must be a list of nodes", TypeError)
            self.childs += childs

    def isLeaf(self):
        """ Return True if the node is a leaf

        :rtype: True or False
        """
        return len(self.childs) == 0

    def getChild(self, index):
        """ Returns the index-child of the node

        :rtype: child node
        """
        return self.childs[index]

    def getChilds(self):
        """ Return the childs of the node

        .. warning :: use .getChilds()[:] if you'll change the list itself, like using childs.reverse(),
                      otherwise the original genome child order will be changed.

        :rtype: a list of nodes
        """
        return self.childs

    def addChild(self, child):
        """ Adds a child to the node

        :param child: the node to be added
        """
        if type(child) == list:
            self.childs.extend(child)
        else:
            if not isinstance(child, GTreeNodeBase):
                Util.raiseException("The child must be a node", TypeError)
            self.childs.append(child)

    def replaceChild(self, older, newer):
        """ Replaces a child of the node

        :param older: the child to be replaces
        :param newer: the new child which replaces the older
        """
        index = self.childs.index(older)
        self.childs[index] = newer

    def setParent(self, parent):
        """ Sets the parent of the node

        :param parent: the parent node
        """
        self.parent = parent

    def getParent(self):
        """ Get the parent node of the node

        :rtype: the parent node
        """
        return self.parent

    def __repr__(self):
        str_repr = "GTreeNodeBase [Childs=%d]" % len(self)
        return str_repr

    def __len__(self):
        return len(self.childs)

    def copy(self, g):
        """ Copy the current contents GTreeNodeBase to 'g'

        :param g: the destination node

        .. note:: If you are planning to create a new chromosome representation, you
                  **must** implement this method on your class.
        """
        g.parent = self.parent
        g.childs = self.childs[:]

    def clone(self):
        """ Clone this GenomeBase

        :rtype: the clone genome

        .. note:: If you are planning to create a new chromosome representation, you
                  **must** implement this method on your class.
        """
        newcopy = GTreeNodeBase(None)
        self.copy(newcopy)
        return newcopy


