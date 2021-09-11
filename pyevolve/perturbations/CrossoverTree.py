
# Tree

def GTreeCrossoverSinglePoint(genome, **args):
    """ The crossover for GTree, Single Point """
    sister = None
    brother = None
    gMom = args["mom"].clone()
    gDad = args["dad"].clone()

    gMom.resetStats()
    gDad.resetStats()

    node_mom_stack = []
    all_mom_nodes = []
    node_mom_tmp = None

    node_dad_stack = []
    all_dad_nodes = []
    node_dad_tmp = None

    node_mom_stack.append(gMom.getRoot())
    node_dad_stack.append(gDad.getRoot())

    while (len(node_mom_stack) > 0) and (len(node_dad_stack) > 0):
        node_mom_tmp = node_mom_stack.pop()
        node_dad_tmp = node_dad_stack.pop()

        if node_mom_tmp != gMom.getRoot():
            all_mom_nodes.append(node_mom_tmp)
            all_dad_nodes.append(node_dad_tmp)

        node_mom_stack.extend(node_mom_tmp.getChilds())
        node_dad_stack.extend(node_dad_tmp.getChilds())

    if len(all_mom_nodes) == 0 or len(all_dad_nodes) == 0:
        return (gMom, gDad)

    if len(all_dad_nodes) == 1:
        nodeDad = all_dad_nodes[0]
    else:
        nodeDad = rand_choice(all_dad_nodes)

    if len(all_mom_nodes) == 1:
        nodeMom = all_mom_nodes[0]
    else:
        nodeMom = rand_choice(all_mom_nodes)

    nodeMom_parent = nodeMom.getParent()
    nodeDad_parent = nodeDad.getParent()

    # Sister
    if args["count"] >= 1:
        sister = gMom
        nodeDad.setParent(nodeMom_parent)
        nodeMom_parent.replaceChild(nodeMom, nodeDad)
        sister.processNodes()

    # Brother
    if args["count"] == 2:
        brother = gDad
        nodeMom.setParent(nodeDad_parent)
        nodeDad_parent.replaceChild(nodeDad, nodeMom)
        brother.processNodes()

    return (sister, brother)


def GTreeCrossoverSinglePointStrict(genome, **args):
    """ The crossover of Tree, Strict Single Point

    ..note:: This crossover method creates offspring with restriction of the
             *max_depth* parameter.

    Accepts the *max_attempt* parameter, *max_depth* (required), and
    the distr_leaft (>= 0.0 and <= 1.0), which represents the probability
    of leaf selection when findin random nodes for crossover.

    """
    sister = None
    brother = None

    gMom = args["mom"].clone()
    gDad = args["dad"].clone()

    gMom.resetStats()
    gDad.resetStats()

    max_depth = gMom.getParam("max_depth", None)
    max_attempt = gMom.getParam("max_attempt", 10)
    distr_leaf = gMom.getParam("distr_leaf", None)

    if max_depth is None:
        Util.raiseException("You must specify the max_depth genome parameter !", ValueError)

    if max_depth < 0:
        Util.raiseException(
            "The max_depth must be >= 1, if you want to use GTreeCrossoverSinglePointStrict crossover !", ValueError)

    momRandom = None
    dadRandom = None

    for i in range(max_attempt):

        if distr_leaf is None:
            dadRandom = gDad.getRandomNode()
            momRandom = gMom.getRandomNode()
        else:
            if Util.randomFlipCoin(distr_leaf):
                momRandom = gMom.getRandomNode(1)
            else:
                momRandom = gMom.getRandomNode(2)

            if Util.randomFlipCoin(distr_leaf):
                dadRandom = gDad.getRandomNode(1)
            else:
                dadRandom = gDad.getRandomNode(2)

        assert momRandom is not None
        assert dadRandom is not None

        # Optimize here
        mH = gMom.getNodeHeight(momRandom)
        dH = gDad.getNodeHeight(dadRandom)

        mD = gMom.getNodeDepth(momRandom)
        dD = gDad.getNodeDepth(dadRandom)

        # The depth of the crossover is greater than the max_depth
        if (dD + mH <= max_depth) and (mD + dH <= max_depth):
            break

    if i == (max_attempt - 1):  # TODO i can be undefined
        assert gMom.getHeight() <= max_depth
        return (gMom, gDad)
    else:
        nodeMom, nodeDad = momRandom, dadRandom

    nodeMom_parent = nodeMom.getParent()
    nodeDad_parent = nodeDad.getParent()

    # Sister
    if args["count"] >= 1:
        sister = gMom
        nodeDad.setParent(nodeMom_parent)

        if nodeMom_parent is None:
            sister.setRoot(nodeDad)
        else:
            nodeMom_parent.replaceChild(nodeMom, nodeDad)
        sister.processNodes()
        assert sister.getHeight() <= max_depth

    # Brother
    if args["count"] == 2:
        brother = gDad
        nodeMom.setParent(nodeDad_parent)

        if nodeDad_parent is None:
            brother.setRoot(nodeMom)
        else:
            nodeDad_parent.replaceChild(nodeDad, nodeMom)
        brother.processNodes()
        assert brother.getHeight() <= max_depth

    return (sister, brother)


# GTreeGP Crossovers

def GTreeGPCrossoverSinglePoint(genome, **args):
    """ The crossover of the GTreeGP, Single Point for Genetic Programming

    ..note:: This crossover method creates offspring with restriction of the
             *max_depth* parameter.

    Accepts the *max_attempt* parameter, *max_depth* (required).
    """
    from . import Consts

    sister = None
    brother = None

    gMom = args["mom"].clone()
    gDad = args["dad"].clone()

    gMom.resetStats()
    gDad.resetStats()

    max_depth = gMom.getParam("max_depth", None)
    max_attempt = gMom.getParam("max_attempt", 15)

    if max_depth is None:
        Util.raiseException("You must specify the max_depth genome parameter !", ValueError)

    if max_depth < 0:
        Util.raiseException(
            "The max_depth must be >= 1, if you want to use GTreeCrossoverSinglePointStrict crossover !", ValueError)

    momRandom = None
    dadRandom = None

    for i in range(max_attempt):

        dadRandom = gDad.getRandomNode()

        if dadRandom.getType() == Consts.nodeType["TERMINAL"]:
            momRandom = gMom.getRandomNode(1)
        elif dadRandom.getType() == Consts.nodeType["NONTERMINAL"]:
            momRandom = gMom.getRandomNode(2)

        mD = gMom.getNodeDepth(momRandom)
        dD = gDad.getNodeDepth(dadRandom)

        # Two nodes are root
        if mD == 0 and dD == 0:
            continue

        mH = gMom.getNodeHeight(momRandom)
        if dD + mH > max_depth:
            continue

        dH = gDad.getNodeHeight(dadRandom)
        if mD + dH > max_depth:
            continue

        break

    if i == (max_attempt - 1):
        assert gMom.getHeight() <= max_depth
        return (gMom, gDad)
    else:
        nodeMom, nodeDad = momRandom, dadRandom

    nodeMom_parent = nodeMom.getParent()
    nodeDad_parent = nodeDad.getParent()

    # Sister
    if args["count"] >= 1:
        sister = gMom
        nodeDad.setParent(nodeMom_parent)

        if nodeMom_parent is None:
            sister.setRoot(nodeDad)
        else:
            nodeMom_parent.replaceChild(nodeMom, nodeDad)
        sister.processNodes()
        assert sister.getHeight() <= max_depth

    # Brother
    if args["count"] == 2:
        brother = gDad
        nodeMom.setParent(nodeDad_parent)

        if nodeDad_parent is None:
            brother.setRoot(nodeMom)
        else:
            nodeDad_parent.replaceChild(nodeDad, nodeMom)
        brother.processNodes()
        assert brother.getHeight() <= max_depth

    return (sister, brother)
