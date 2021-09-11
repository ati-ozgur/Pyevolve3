from random import choice as rand_choice
import inspect

from ..FunctionSlot import FunctionSlot
from .. import Util

from .GenomeBase import GenomeBase


class G1DBase(GenomeBase):
    """ G1DBase Class - The base class for 1D chromosomes

    This chromosome class extends the :class:`GenomeBase` classes.

    :param size: the 1D list size

    .. versionadded:: 0.6
       Added the *G1DBase* class
    """
    __slots__ = ["genomeSize", "genomeList"]

    def __init__(self, size):
        super(G1DBase, self).__init__()
        self.genomeSize = size
        self.genomeList = []

    def __iadd__(self, item):
        """ To add more items using the += operator """
        self.genomeList.append(item)
        return self

    def __eq__(self, other):
        """ Compares one chromosome with another """
        cond1 = (self.genomeList == other.genomeList)
        cond2 = (self.genomeSize == other.genomeSize)
        return True if cond1 and cond2 else False

    def __contains__(self, value):
        """ Used on: *value in genome* """
        return value in self.genomeList
    # These methods are correctly overrided in every child class
    # Deprecated in Python 3

    # def __getslice__(self, a, b):
    #     """ Return the sliced part of chromosome """
    #     return self.genomeList[a:b]
    #
    # def __setslice__(self, a, b, val):
    #     """ Sets the slice part of chromosome """
    #     self.genomeList[a:b] = val

    def __getitem__(self, key):
        """ Return the specified gene of List """
        return self.genomeList[key]

    def __setitem__(self, key, value):
        """ Set the specified value for an gene of List """
        self.genomeList[key] = value

    def __iter__(self):
        """ Iterator support to the list """
        return iter(self.genomeList)

    def __len__(self):
        """ Return the size of the List """
        return len(self.genomeList)

    def getListSize(self):
        """ Returns the list supposed size

        .. warning:: this is different from what the len(obj) returns
        """
        return self.genomeSize

    def resumeString(self):
        """ Returns a resumed string representation of the Genome """
        return str(self.genomeList)

    def append(self, value):
        """ Appends an item to the end of the list

        Example:
           >>> genome.append(44)

        :param value: value to be added

        """
        self.genomeList.append(value)

    def remove(self, value):
        """ Removes an item from the list

        Example:
           >>> genome.remove(44)

        :param value: value to be added

        """
        self.genomeList.remove(value)

    def clearList(self):
        """ Remove all genes from Genome """
        del self.genomeList[:]

    def copy(self, g):
        """ Copy genome to 'g'

        Example:
           >>> genome_origin.copy(genome_destination)

        :param g: the destination instance

        """
        g.genomeSize = self.genomeSize
        g.genomeList = self.genomeList[:]

    def getInternalList(self):
        """ Returns the internal list of the genome

        ... note:: this method was created to solve performance issues
        :rtype: the internal list
        """
        return self.genomeList

    def setInternalList(self, lst):
        """ Assigns a list to the internal list of the chromosome

        :param lst: the list to assign the internal list of the chromosome
        """
        self.genomeList = lst
