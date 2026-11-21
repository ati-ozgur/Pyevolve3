"""Bundled TSPLIB (TSP) and CVRP problem instances.

The instances ship inside the package under ``pyevolve/planning/data``:

- ``data/tsp/<name>.tsp`` (plus a few ``.opt.tour`` optimal tours)
- ``data/vrp/small/<name>.vrp`` and ``data/vrp/big/<name>.vrp``

Loading requires the optional ``tsplib95`` dependency
(``pip install "Pyevolve3[planning]"``).
"""

from importlib.resources import files


DATA_ROOT = files("pyevolve.planning") / "data"


def _import_tsplib95():
    try:
        import tsplib95
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "Loading TSPLIB/CVRP instances requires tsplib95. "
            'Install it with: pip install "Pyevolve3[planning]"'
        ) from exc
    return tsplib95


def _resource(*parts):
    resource = DATA_ROOT.joinpath(*parts)
    if not resource.is_file():
        raise FileNotFoundError(f"Bundled dataset not found: {'/'.join(parts)}")
    return resource


def list_tsp_problems():
    """Return the sorted names of all bundled TSP instances (without ``.tsp``)."""
    return sorted(
        entry.name[: -len(".tsp")]
        for entry in DATA_ROOT.joinpath("tsp").iterdir()
        if entry.name.endswith(".tsp")
    )


def list_vrp_problems(size="small"):
    """Return the sorted names of bundled CVRP instances; ``size`` is ``"small"`` or ``"big"``."""
    return sorted(
        entry.name[: -len(".vrp")]
        for entry in DATA_ROOT.joinpath("vrp", size).iterdir()
        if entry.name.endswith(".vrp")
    )


def load_tsp_problem(problem_name):
    """Load a bundled TSP instance as a ``tsplib95`` problem."""
    tsplib95 = _import_tsplib95()
    text = _resource("tsp", f"{problem_name}.tsp").read_text()
    return tsplib95.parse(text)


def load_vrp_problem(problem_name, size="small"):
    """Load a bundled CVRP instance as a ``tsplib95`` problem."""
    tsplib95 = _import_tsplib95()
    text = _resource("vrp", size, f"{problem_name}.vrp").read_text()
    return tsplib95.parse(text)
