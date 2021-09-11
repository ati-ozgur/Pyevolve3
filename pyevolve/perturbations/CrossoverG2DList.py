

# 2D List

def G2DListCrossoverUniform(genome, **args):
    """ The G2DList Uniform Crossover """
    from . import Consts
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    sister = gMom.clone()
    brother = gDad.clone()
    sister.resetStats()
    brother.resetStats()

    h, w = gMom.getSize()

    for i in range(h):
        for j in range(w):
            if Util.randomFlipCoin(Consts.CDefG2DListCrossUniformProb):
                temp = sister.getItem(i, j)
                sister.setItem(i, j, brother.getItem(i, j))
                brother.setItem(i, j, temp)

    return (sister, brother)


def G2DListCrossoverSingleVPoint(genome, **args):
    """ The crossover of G2DList, Single Vertical Point """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    cut = rand_randint(1, gMom.getWidth() - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        for i in range(sister.getHeight()):
            sister[i][cut:] = gDad[i][cut:]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        for i in range(brother.getHeight()):
            brother[i][cut:] = gMom[i][cut:]

    return (sister, brother)


def G2DListCrossoverSingleHPoint(genome, **args):
    """ The crossover of G2DList, Single Horizontal Point """
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    cut = rand_randint(1, gMom.getHeight() - 1)

    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        for i in range(cut, sister.getHeight()):
            sister[i][:] = gDad[i][:]

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        for i in range(brother.getHeight()):
            brother[i][:] = gMom[i][:]

    return (sister, brother)
