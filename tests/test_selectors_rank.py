from types import SimpleNamespace

from pyevolve.selections.Selectors import GRankSelector


class Individual:
    def __init__(self, fitness, score):
        self.fitness = fitness
        self.score = score


class FakePopulation:
    def __init__(self, individuals, sortType):
        self.internalPop = individuals
        self._list = individuals
        self.sortType = sortType

    def __len__(self):
        return len(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def bestFitness(self):
        best = max(ind.fitness for ind in self._list)
        return SimpleNamespace(fitness=best)

    def bestRaw(self):
        best = max(ind.score for ind in self._list)
        return SimpleNamespace(score=best)


def test_grankselector_scaled():
    from pyevolve import Consts

    # reset cache to avoid cross-test interference
    GRankSelector.cachePopID = None
    GRankSelector.cacheIndices = None

    inds = [Individual(10, 1), Individual(20, 2), Individual(20, 3)]
    pop = FakePopulation(inds, Consts.sortType["scaled"])

    selected = GRankSelector(pop, popID="p1")
    assert selected.fitness == 20


def test_grankselector_raw():
    from pyevolve import Consts

    # reset cache to avoid cross-test interference
    GRankSelector.cachePopID = None
    GRankSelector.cacheIndices = None

    inds = [Individual(5, 8), Individual(4, 9), Individual(3, 9)]
    pop = FakePopulation(inds, Consts.sortType["raw"])

    selected = GRankSelector(pop, popID="raw1")
    assert selected.score == 9
