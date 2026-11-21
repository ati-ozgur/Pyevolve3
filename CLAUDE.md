# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Pyevolve3 is a Python 3 port of the Pyevolve genetic algorithm framework (forked from BubaVV/Pyevolve, originally perone/Pyevolve). Current development focus is on additional GA operators, especially permutation operators for the Traveling Salesperson Problem (TSP) and related routing problems (CVRP). Minimum Python is 3.9; CI tests 3.9–3.13 (`mise.toml` pins 3.13 locally).

## Commands

```bash
pip install -e ".[test,examples]"              # packaging is pyproject.toml only (setuptools backend)
python -m build                                # sdist + wheel (needs `pip install build`)

pytest                                         # full test suite (what CI runs)
pytest tests/test_crossovers_G1DListTsp.py     # single file
pytest tests/test_mutators.py::G1DBinaryStringMutatorsTestCase::test_swap_mutator_small_pmut  # single test (Class::method)
tox                                            # py39..py313

# Lint: CI fails only on syntax errors / undefined names, the rest is report-only
flake8 --config=tox.ini . --count --select=E9,F63,F7,F82 --show-source --statistics
ruff check .                                   # ruff config in pyproject.toml (line-length 120, mccabe 10)

# Examples (CI runs these via manual workflow_dispatch only)
python examples/pyevolve_ex_tsp_01.py
for f in examples/pyevolve_ex_tsp_*; do python "$f"; done

# Docs (Quarto + quartodoc, published to GitHub Pages from docs/source)
python docs/source/generate_examples.py        # regenerates docs/source/examples.md from example docstrings
docs/build_docs.sh                             # quartodoc build && quarto render
```

Dependencies: the core library only requires numpy. Extras in `pyproject.toml`: `graph` (matplotlib), `planning` (tsplib95, Pillow, scipy, scikit-fuzzy — needed by `pyevolve.planning`), `examples` (`graph` + `planning`), `test`. The package version comes from `pyevolve.__version__`.

## Architecture

### Engine / population / genome, wired together by FunctionSlots

- `pyevolve/GSimpleGA.py` — `GSimpleGA` engine. `evolve()` loops `step()`; each step clones the population, selects pairs, applies crossover (always if `pCrossover >= 1.0`, else by coin flip), mutates, evaluates, applies elitism (respecting `minimax`), and sorts. Termination is via `nGenerations`, `setMaxTime`, or the `terminationCriteria` slot (e.g. `RawScoreCriteria`, `ConvergenceCriteria`). `stepCallback` slot runs every generation.
- `pyevolve/GPopulation.py` — holds individuals, evaluation (optional multiprocessing), scaling, sorting, statistics.
- `pyevolve/representations/GenomeBase.py` — every genome has four `FunctionSlot`s: `evaluator`, `initializator`, `mutator`, `crossover`. Genome types: `G1DList`, `G1DBinaryString`, `G2DList`, `G2DBinaryString`, `GTree` (incl. GP trees), plus `GAllele` for per-position allele sets.
- `pyevolve/FunctionSlot.py` — the plugin mechanism. Operators are **plain functions** assigned with `slot.set(fn)` / `slot += fn`, not subclasses. Signatures:
  - initializator: `fn(genome, **args)`
  - mutator: `fn(genome, **args)` → returns number of mutations (`args["pmut"]`, `args["ga_engine"]`)
  - crossover: `fn(genome, **args)` → `(sister, brother)`; uses `args["mom"]`, `args["dad"]`, `args["count"]` (1 or 2; `None` for a child not requested)
  - selector: `fn(population, **args)` → individual
  - evaluator: `fn(genome)` → score
- `pyevolve/Consts.py` — all defaults (`CDefGA*`, default operators per genome type, `minimaxType`, `CDefRangeMin/Max`, etc.). Defaults for a new operator/genome usually belong here.

### Operator packages

- `perturbations/` — crossovers and mutators, one module per genome type. TSP/permutation work lives in `CrossoverG1DListTspPermutations.py` (OX, OX2, PMX, EPMX, Cycle, POS, MPX, Edge, CutCrossfill, Greedy, IGX, Sequential Constructive, …), `CrossoverG1DListTspPermutations2.py`, `MutatorG1DListPermutations.py`, with helpers `DoublyCircularLinkedList.py` and `G1DListCrossoverSRX_Helper.py`. Permutation crossovers must produce valid tours (`checkTspListIntegrity`).
- `selections/` — `Selectors.py` (roulette, tournament, rank, uniform, …) and `SelectionRank.py`.
- `initializations/` — per-genome initializers; `InitializationPermutations.py` for TSP random tours.

### Passing problem data to operators

Operators receive data through parameter dicts, not globals:
- `genome.setParams(...)` → read in operators via `genome.getParam(key, default)` or `genome.internalParams`. Distance-aware TSP crossovers (e.g. Greedy, IGX, SCX) require `distance_matrix_list` / `distance_matrix_dict` set on the genome and raise `ValueError` otherwise. Params are copied on `clone()`, so every individual sees them.
- `ga.setParams(...)` → read from `ga_engine.getParam(...)` in callbacks/termination criteria.

### Planning package (TSP/CVRP harness and datasets)

- `pyevolve/planning/` holds the TSP/CVRP experiment code and data that ships with the package (extra `planning`: tsplib95, Pillow, scikit-fuzzy, scipy; all imported lazily so core `pyevolve` stays numpy-only).
- `planning/datasets.py` loads the bundled instances via `importlib.resources`: `data/tsp/*.tsp` (`load_tsp_problem`), `data/vrp/{small,big}/*.vrp` (`load_vrp_problem`). Non-standard CVRP files (Golden_*, Li_*: depot given as coordinates, `EDGE_WEIGHT_TYPE: FUNCTION`) are normalized in memory by `_normalize_vrp_text` (depot → node 0, exact Euclidean distances).
- `planning/tsp_helper.py` → `run_tsp(problem_name, crossover_method, mutation_method, selection_method, ...)` is the shared driver for the `pyevolve_ex_tsp_*` experiments: it loads a bundled TSPLIB instance (or generates random cities when `problem_name` contains "random"), sets distance matrices on the genome, minimizes tour length, logs results to `./experiments` and (with Pillow) writes tour images to `./tsp_img` — both relative to the current working directory. `crossover_method` may be a string key into `dict_crossoever_operators` or a function.
- `planning/selector_helper.py` is the analogous harness for adaptive-selector experiments (`run_selector_ga`, `run_experiment_series`); `planning/cvrp.py` has `load_cvrp_instance` / `make_cvrp_fitness`.
- Public names are re-exported from `pyevolve.planning` (e.g. `from pyevolve.planning import run_tsp`).

### Examples

- `examples/pyevolve_ex*.py` are the demos; their module docstrings are rendered into the docs by `docs/source/generate_examples.py`. TSP/CVRP examples import from `pyevolve.planning`.

### Other

- `DBAdapters.py` — stats output adapters (CSV, SQLite → `pyevolve.db`, URL post, VPython, MySQL); `pyevolve/graph.py` (installed as the `pyevolve_graph` command) plots from the SQLite DB.
- `Interaction.py` — interactive mode hooks; `Scaling.py` — fitness scaling functions; `Statistics.py`; `Util.py` — random helpers (`randomFlipCoin`, etc.) and `raiseException`.

## Tests

Tests are `unittest.TestCase` classes run with pytest. Operator tests patch the module-level random functions imported into the operator module (e.g. `@patch('pyevolve.perturbations.CrossoverG1DList.rand_randint')`) and feed deterministic `side_effect` sequences, so when adding an operator keep `from random import randint as rand_randint`-style module-level imports to stay mockable. Crossover tests subclass `CrossoverTestCase` from `tests/test_crossovers.py` (`assertCrossoverResultsEqual`).
