"""
    ## `GTree` and GTreeGP -- the tree chromosomes

    This is the rooted tree representation, this chromosome representation
    can carry any data-type.

    ### Default Parameters

    *Initializator*

      `Initializators.GTreeInitializatorInteger`

       The Integer Initializator for GTree

    *Mutator*

       `Mutators.GTreeMutatorIntegerRange`

       The Integer Range mutator for GTree

    *Crossover*

       `Crossovers.GTreeCrossoverSinglePointStrict`

       The Strict Single Point crossover for GTree

    ::: {.callout-note title="Added in version 0.6"}
    The *GTree* module.
    :::

    ### Classes
"""
import random
from .GenomeBase import GenomeBase
from .GTreeBase import GTreeBase
from .GTreeNodeBase import GTreeNodeBase
from .. import Util
from .. import Consts

try:
    import pydot_ng as pydot
    HAVE_PYDOT = True
except ImportError:
    HAVE_PYDOT = False

#################################
#             GTree             #
#################################


class GTree(GTreeBase):
    """
        The GTree class - The tree chromosome representation

        Inheritance diagram: ``GTree.GTree``


        ### Parameters

        - `root_node`: the root node of the tree
    """

    def __init__(self, root_node=None):

        super(GTree, self).__init__(root_node)
        from .. import ConstsTree

        self.initializator.set(ConstsTree.CDefGTreeInit)
        self.mutator.set(ConstsTree.CDefGGTreeMutator)
        self.crossover.set(ConstsTree.CDefGTreeCrossover)

    def __repr__(self):
        """
            Return a string representation of Genome
        """
        ret = GenomeBase.__repr__(self)
        ret += GTreeBase.__repr__(self)
        return ret

    def copy(self, g):
        """
            Copy the contents to the destination g

            ### Parameters

            - `g`: the GTree genome destination
        """
        GenomeBase.copy(self, g)
        GTreeBase.copy(self, g)

    def clone(self):
        """
            Return a new instance of the genome

            ### Returns

            new GTree instance
        """
        newcopy = GTree()
        self.copy(newcopy)
        newcopy.processNodes(True)
        return newcopy


class GTreeNode(GTreeNodeBase):
    """
        The GTreeNode class - The node representation

        Inheritance diagram: ``GTree.GTreeNode``


        ### Parameters

        - `data`: the root node of the tree
        - `parent`: the parent node, if root, this
                         must be *None*
    """
    __slots__ = ["node_data"]

    def __init__(self, data, parent=None):
        super(GTreeNode, self).__init__(parent)
        self.node_data = data

    def __repr__(self):
        str_repr = GTreeNodeBase.__repr__(self)
        str_repr += " - [%s]" % self.node_data
        return str_repr

    def setData(self, data):
        """
            Sets the data of the node

            ### Parameters

            - `data`: the data of the node
        """
        self.node_data = data

    def getData(self):
        """
            Return the data of the node

            ### Returns

            the data of the node
        """
        return self.node_data

    def newNode(self, data):
        """
            Created a new child node

            ### Parameters

            - `data`: the data of the new created node
        """
        node = GTreeNode(data, self)
        self.addChild(node)
        return node

    def swapNodeData(self, node):
        """
            Swaps the node data with another node

            ### Parameters

            - `node`: the node to do the data swap
        """
        tmp_data = self.node_data
        self.setData(node.getData())
        node.setData(tmp_data)

    def copy(self, g):
        """
            Copy the contents to the destination g

            ### Parameters

            - `g`: the GTreeNode genome destination
        """
        GTreeNodeBase.copy(self, g)
        g.node_data = self.node_data

    def clone(self):
        """
            Return a new instance of the genome

            ### Returns

            new GTree instance
        """
        newcopy = GTreeNode(None)
        self.copy(newcopy)
        return newcopy

#################################
#    Tree Utility Functions     #
#################################


def buildGTreeGrow(depth, value_callback, max_siblings, max_depth):
    """
        Random generates a Tree structure using the value_callback
        for data generation and the method "Grow"

        ### Parameters

        - `depth`: the initial depth, zero
        - `value_callback`: the function which generates the random
                                 values for nodes
        - `max_siblings`: the maximum number of sisters of a node
        - `max_depth`: the maximum depth of the tree

        ### Returns

        the root node of created tree
    """

    random_value = value_callback()
    n = GTreeNode(random_value)

    if depth == max_depth:
        return n

    for i in range(random.randint(0, abs(max_siblings))):
        child = buildGTreeGrow(depth + 1, value_callback, max_siblings, max_depth)
        child.setParent(n)
        n.addChild(child)
    return n


def buildGTreeFull(depth, value_callback, max_siblings, max_depth):
    """
        Random generates a Tree structure using the value_callback
        for data generation and the method "Full"

        ### Parameters

        - `depth`: the initial depth, zero
        - `value_callback`: the function which generates the random
                                 values for nodes
        - `max_siblings`: the maximum number of sisters of a node
        - `max_depth`: the maximum depth of the tree

        ### Returns

        the root node of created tree
    """

    random_value = value_callback()
    n = GTreeNode(random_value)

    if depth == max_depth:
        return n

    if max_siblings < 0:
        range_val = abs(max_siblings)
    else:
        range_val = random.randint(1, abs(max_siblings))

    for i in range(range_val):
        child = buildGTreeFull(depth + 1, value_callback, max_siblings, max_depth)
        child.setParent(n)
        n.addChild(child)
    return n

#################################
#             GTree   GP        #
#################################


class GTreeNodeGP(GTreeNodeBase):
    """
        The GTreeNodeGP Class - The Genetic Programming Node representation

        Inheritance diagram: ``GTree.GTreeNodeGP``


        ### Parameters

        - `data`: the node data
        - `type`: the node type
        - `parent`: the node parent
    """
    __slots__ = ["node_type", "node_data"]

    def __init__(self, data, node_type=0, parent=None):
        super(GTreeNodeGP, self).__init__(parent)
        self.node_type = node_type
        self.node_data = data

    def __repr__(self):
        str_repr = GTreeNodeBase.__repr__(self)
        str_repr += " - [%s]" % self.node_data
        return str_repr

    def compare(self, other):
        """
            Compare this node with other

            ### Parameters

            - `other`: the other GTreeNodeGP
        """
        if not isinstance(other, GTreeNodeGP):
            Util.raiseException("The other node used to compare is not a GTreeNodeGP class", TypeError)

        if other.node_type == self.node_type:
            if other.node_data == self.node_data:
                return 0
        return -1

    def setData(self, data):
        """
            Sets the node internal data

            ### Parameters

            - `data`: the internal data
        """
        self.node_data = data

    def getData(self):
        """
            Gets the node internal data

            ### Returns

            the internal data
        """
        return self.node_data

    def setType(self, node_type):
        """
            Sets the node type

            ### Parameters

            - `node_type`: the node type is type of Consts.nodeType
        """
        self.node_type = node_type

    def getType(self):
        """
            Get the node type

            ### Returns

            the node type is type of Consts.nodeType
        """
        return self.node_type

    def newNode(self, data):
        """
            Creates a new node and adds this
            node as children of current node

            ### Parameters

            - `data`: the internal node data
        """
        node = GTreeNodeGP(data, self)
        self.addChild(node)
        return node

    def swapNodeData(self, node):
        """
            Swaps the node data and type with another node

            ### Parameters

            - `node`: the node
        """
        tmp_data = self.node_data
        tmp_type = self.node_type
        self.setData(node.getData())
        self.setType(node.getType())
        node.setData(tmp_data)
        node.setType(tmp_type)

    def copy(self, g):
        """
            Copy the contents to the destination g

            ### Parameters

            - `g`: the GTreeNodeGP genome destination
        """
        GTreeNodeBase.copy(self, g)
        g.node_data = self.node_data
        g.node_type = self.node_type

    def clone(self):
        """
            Return a new copy of the node

            ### Returns

            the new GTreeNodeGP instance
        """
        newcopy = GTreeNodeGP(None)
        self.copy(newcopy)
        return newcopy


class GTreeGP(GTreeBase):
    """
        The GTreeGP Class - The Genetic Programming Tree representation

        Inheritance diagram: ``GTree.GTreeGP``


        ### Parameters

        - `root_node`: the Root node of the GP Tree
    """

    def __init__(self, root_node=None, cloning=False):

        super(GTreeGP, self).__init__(root_node)
        if not cloning:
            from .. import ConstsTree

            self.initializator.set(ConstsTree.CDefGTreeGPInit)
            self.mutator.set(ConstsTree.CDefGGTreeGPMutator)
            self.crossover.set(ConstsTree.CDefGTreeGPCrossover)

    def __repr__(self):
        """
            Return a string representation of Genome
        """
        ret = GenomeBase.__repr__(self)
        ret += GTreeBase.__repr__(self)
        ret += "\n- GTreeGP\n"
        ret += "\tExpression: %s\n" % self.getPreOrderExpression()
        return ret

    def writeDotImage(self, filename):
        """
            Writes a image representation of the individual

            ### Parameters

            - `filename`: the output file image
        """
        if not HAVE_PYDOT:
            Util.raiseException("You must install Pydot to use this feature !")

        graph = pydot.Dot()
        self.writeDotGraph(graph)
        graph.write_jpeg(filename, prog='dot')

    def writeDotRaw(self, filename):
        """
            Writes the raw dot file (text-file used by dot/neato) with the
            representation of the individual

            ### Parameters

            - `filename`: the output file, ex: individual.dot
        """
        if not HAVE_PYDOT:
            Util.raiseException("You must install Pydot to use this feature !")

        graph = pydot.Dot(graph_type="digraph")
        self.writeDotGraph(graph)
        graph.write(filename, prog='dot', format="raw")

    def writeDotGraph(self, graph, startNode=0):
        """
            Write a graph to the pydot Graph instance

            ### Parameters

            - `graph`: the pydot Graph instance
            - `startNode`: used to plot more than one individual
        """

        if not HAVE_PYDOT:
            print("You must install Pydot to use this feature !")
            return

        count = startNode
        node_stack = []
        nodes_dict = {}
        import __main__ as main_module

        for i in range(len(self.nodes_list)):
            newnode = pydot.Node(str(count), style="filled")
            count += 1

            if self.nodes_list[i].getType() == Consts.nodeType["TERMINAL"]:
                newnode.set_color("lightblue2")
            else:
                newnode.set_color("goldenrod2")

            if self.nodes_list[i].getType() == Consts.nodeType["NONTERMINAL"]:
                func = getattr(main_module, self.nodes_list[i].getData())

                if hasattr(func, "shape"):
                    newnode.set_shape(func.shape)

                if hasattr(func, "representation"):
                    newnode.set_label(func.representation)
                else:
                    newnode.set_label(self.nodes_list[i].getData())
                if hasattr(func, "color"):
                    newnode.set_color(func.color)

            else:
                newnode.set_label(self.nodes_list[i].getData())

            nodes_dict.update({self.nodes_list[i]: newnode})
            graph.add_node(newnode)

        node_stack.append(self.getRoot())
        while len(node_stack) > 0:
            tmp = node_stack.pop()

            parent = tmp.getParent()
            if parent is not None:
                parent_node = nodes_dict[parent]
                child_node = nodes_dict[tmp]

                newedge = pydot.Edge(parent_node, child_node)
                graph.add_edge(newedge)

            rev_childs = tmp.getChilds()[:]
            rev_childs.reverse()
            node_stack.extend(rev_childs)

        return count

    def getSExpression(self, start_node=None):
        """
            Returns a tree-formated string (s-expression) of the tree.

            ### Returns

            a S-Expression representing the tree
        """
        str_buff = ""
        if start_node is None:
            start_node = self.getRoot()
            str_buff += "%s " % start_node.getData()

        is_leaf = start_node.isLeaf()
        if not is_leaf:
            str_buff += "( "

        for child_node in start_node.getChilds():
            str_buff += "%s " % child_node.getData()
            str_buff += self.getSExpression(child_node)

        if not is_leaf:
            str_buff += " )"
        return str_buff

    def getPreOrderExpression(self, start_node=None):
        """
            Return the pre order expression string of the Tree, used
            to python *eval*.

            ### Returns

            the expression string
        """
        if start_node is None:
            start_node = self.getRoot()

        str_buff = start_node.getData()

        if not start_node.isLeaf():
            all_childs = start_node.getChilds()
            str_buff += "(" + self.getPreOrderExpression(all_childs[0])

            for index in range(1, len(all_childs)):
                child = all_childs[index]
                str_buff += ", " + self.getPreOrderExpression(child)
            str_buff += ")"

        return str_buff

    def getCompiledCode(self):
        """
            Get the compiled code for the Tree expression
            After getting the compiled code object, you just need to evaluate it using
            the `eval` native Python method.

            ### Returns

            compiled python code
        """
        expr = self.getPreOrderExpression()
        return compile(expr, "<string>", "eval")

    def copy(self, g):
        """
            Copy the contents to the destination g

            ### Parameters

            - `g`: the GTreeGP genome destination
        """
        GenomeBase.copy(self, g)
        GTreeBase.copy(self, g)

    def clone(self):
        """
            Return a new instance of the genome

            ### Returns

            the new GTreeGP instance
        """
        newcopy = GTreeGP(cloning=True)
        self.copy(newcopy)
        newcopy.processNodes(True)
        return newcopy

    def compare(self, other):
        """
            This method will compare the currently tree with another one

            ### Parameters

            - `other`: the other GTreeGP to compare
        """
        if not isinstance(other, GTreeGP):
            Util.raiseException("The other tree used to compare is not a GTreeGP class", TypeError)

        stack_self = []
        stack_other = []

        stack_self.append(self.getRoot())
        stack_other.append(other.getRoot())

        while len(stack_self) > 0:

            if (len(stack_self) <= 0) or (len(stack_other) <= 0):
                return -1

            tmp_self, tmp_other = stack_self.pop(), stack_other.pop()
            if tmp_self.compare(tmp_other) != 0:
                return -1

            stack_self.extend(tmp_self.getChilds())
            stack_other.extend(tmp_other.getChilds())

        return 0

    @staticmethod
    def writePopulationDot(ga_engine, filename, format="jpeg", start=0, end=0):
        """
            Writes to a graphical file using pydot, the population of trees

            Example:
            ```pycon
            >>> GTreeGP.writePopulationDot(ga_engine, "pop.jpg", "jpeg", 0, 10)
            ```

            This example will draw the first ten individuals of the population into
            the file called "pop.jpg".

            ### Parameters

            - `ga_engine`: the GA Engine
            - `filename`: the filename, ie. population.jpg
            - `start`: the start index of individuals
            - `end`: the end index of individuals
        """
        if not HAVE_PYDOT:
            Util.raiseException("You must install Pydot to use this feature !")

        pop = ga_engine.getPopulation()
        graph = pydot.Dot(graph_type="digraph")

        if not isinstance(pop[0], GTreeGP):
            Util.raiseException("The population must have individuals of the GTreeGP chromosome !")

        n = 0
        end_index = len(pop) if end == 0 else end
        for i in range(start, end_index):
            ind = pop[i]
            subg = pydot.Cluster(
                "cluster_%d" % i,
                label="\"Ind. #%d - Score Raw/Fit.: %.4f/%.4f\"" % (i, ind.getRawScore(), ind.getFitnessScore())
            )
            n = ind.writeDotGraph(subg, n)
            graph.add_subgraph(subg)

        graph.write(filename, prog='dot', format=format)

    @staticmethod
    def writePopulationDotRaw(ga_engine, filename, start=0, end=0):
        """
            Writes to a raw dot file using pydot, the population of trees

            Example:
            ```pycon
            >>> GTreeGP.writePopulationDotRaw(ga_engine, "pop.dot", 0, 10)
            ```

            This example will draw the first ten individuals of the population into
            the file called "pop.dot".

            ### Parameters

            - `ga_engine`: the GA Engine
            - `filename`: the filename, ie. population.dot
            - `start`: the start index of individuals
            - `end`: the end index of individuals
        """
        if not HAVE_PYDOT:
            Util.raiseException("You must install Pydot to use this feature !")

        pop = ga_engine.getPopulation()
        graph = pydot.Dot(graph_type="digraph")

        if not isinstance(pop[0], GTreeGP):
            Util.raiseException("The population must have individuals of the GTreeGP chromosome !")

        n = 0
        end_index = len(pop) if end == 0 else end
        for i in range(start, end_index):
            ind = pop[i]
            subg = pydot.Cluster(
                "cluster_%d" % i,
                label="\"Ind. #%d - Score Raw/Fit.: %.4f/%.4f\"" % (i, ind.getRawScore(), ind.getFitnessScore())
            )
            n = ind.writeDotGraph(subg, n)
            graph.add_subgraph(subg)

        graph.write(filename, prog='dot', format="raw")


#################################
#    Tree GP Utility Functions  #
#################################

def gpdec(**kwds):
    """ This is a decorator to use with genetic programming non-terminals

    It currently accepts the attributes: shape, color and representation.
    """
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f
    return decorate


def checkTerminal(terminal):
    """
        Do some check on the terminal, to evaluate ephemeral constants

        ### Parameters

        - `terminal`: the terminal string
    """
    if terminal.startswith("ephemeral:"):
        splited = terminal.split(":")
        ephemeral_constant = eval(splited[1])
        return str(ephemeral_constant)
    else:
        return terminal


def buildGTreeGPGrow(ga_engine, depth, max_depth):
    """
        Creates a new random GTreeGP root node with subtrees using
        the "Grow" method.

        ### Parameters

        - `ga_engine`: the GA Core
        - `depth`: the initial depth
        - `max_depth`: the maximum depth of the tree

        ### Returns

        the root node
    """

    gp_terminals = ga_engine.getParam("gp_terminals")
    assert gp_terminals is not None

    gp_function_set = ga_engine.getParam("gp_function_set")
    assert gp_function_set is not None

    if depth == max_depth:
        random_terminal = checkTerminal(random.choice(gp_terminals))
        n = GTreeNodeGP(random_terminal, Consts.nodeType["TERMINAL"])
        return n
    else:
        # Do not generate degenerative trees
        if depth == 0:
            random_node = random.choice(list(gp_function_set.keys()))
        else:
            fchoice = random.choice([list(gp_function_set.keys()), gp_terminals])
            random_node = random.choice(fchoice)

        if random_node in gp_terminals:
            n = GTreeNodeGP(checkTerminal(random_node), Consts.nodeType["TERMINAL"])
        else:
            n = GTreeNodeGP(random_node, Consts.nodeType["NONTERMINAL"])

    if n.getType() == Consts.nodeType["NONTERMINAL"]:
        for i in range(gp_function_set[n.getData()]):
            child = buildGTreeGPGrow(ga_engine, depth + 1, max_depth)
            child.setParent(n)
            n.addChild(child)

    return n


def buildGTreeGPFull(ga_engine, depth, max_depth):
    """
        Creates a new random GTreeGP root node with subtrees using
        the "Full" method.

        ### Parameters

        - `ga_engine`: the GA Core
        - `depth`: the initial depth
        - `max_depth`: the maximum depth of the tree

        ### Returns

        the root node
    """

    gp_terminals = ga_engine.getParam("gp_terminals")
    assert gp_terminals is not None

    gp_function_set = ga_engine.getParam("gp_function_set")
    assert gp_function_set is not None

    if depth == max_depth:
        random_terminal = checkTerminal(random.choice(gp_terminals))
        n = GTreeNodeGP(random_terminal, Consts.nodeType["TERMINAL"])
        return n
    else:
        random_oper = random.choice(list(gp_function_set.keys()))
        n = GTreeNodeGP(random_oper, Consts.nodeType["NONTERMINAL"])

    if n.getType() == Consts.nodeType["NONTERMINAL"]:
        for i in range(gp_function_set[n.getData()]):
            child = buildGTreeGPFull(ga_engine, depth + 1, max_depth)
            child.setParent(n)
            n.addChild(child)

    return n
