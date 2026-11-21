"""Bundled TSPLIB (TSP) and CVRP problem instances.

The instances ship inside the package under ``pyevolve/planning/data``:

- ``data/tsp/<name>.tsp`` (plus a few ``.opt.tour`` optimal tours)
- ``data/vrp/small/<name>.vrp`` and ``data/vrp/big/<name>.vrp``

Loading requires the optional ``tsplib95`` dependency
(``pip install "Pyevolve3[planning]"``).
"""

import re
from importlib.resources import files


DATA_ROOT = files("pyevolve.planning") / "data"

_FUNCTION_WEIGHT_RE = re.compile(r"^EDGE_WEIGHT_TYPE\s*:\s*FUNCTION\s*$", re.MULTILINE)
_EDGE_WEIGHT_FORMAT_RE = re.compile(r"^EDGE_WEIGHT_FORMAT\s*:.*\n", re.MULTILINE)
_DEPOT_COORDS_RE = re.compile(r"(DEPOT_SECTION[ \t]*\n)\s*(-?[\d.]+)\s+(-?[\d.]+)\s*\n")
_SECTION_START_RE = r"(^{}[ \t]*\n)"


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


def _exact_euclidean(start, end):
    """Unrounded 2D Euclidean distance (TSPLIB ``EUC_2D`` rounds to the nearest integer)."""
    from tsplib95 import distances

    return distances.euclidean(start, end, round=lambda value: value)


def _normalize_vrp_text(text):
    """Rewrite non-standard CVRP files (Golden_*, Li_*) into a form tsplib95 can parse.

    These files use ``EDGE_WEIGHT_TYPE: FUNCTION`` / ``EDGE_WEIGHT_FORMAT: EUC_2D`` for unrounded Euclidean
    distances, and give the depot as coordinates in ``DEPOT_SECTION`` instead of a node id.
    The depot becomes node ``0`` with demand ``0``, and the distances become ``SPECIAL`` (exact Euclidean).

    Returns ``(text, special)`` where ``special`` is the distance function to pass to ``tsplib95.parse``.
    """
    if not _FUNCTION_WEIGHT_RE.search(text):
        return text, None

    text = _FUNCTION_WEIGHT_RE.sub("EDGE_WEIGHT_TYPE: SPECIAL", text)
    text = _EDGE_WEIGHT_FORMAT_RE.sub("", text)

    depot = _DEPOT_COORDS_RE.search(text)
    if depot is not None:
        x, y = depot.group(2), depot.group(3)
        text = _DEPOT_COORDS_RE.sub(r"\g<1>0\n", text, count=1)
        text = re.sub(_SECTION_START_RE.format("NODE_COORD_SECTION"), rf"\g<1>0 {x} {y}\n", text,
                      count=1, flags=re.MULTILINE)
        text = re.sub(_SECTION_START_RE.format("DEMAND_SECTION"), r"\g<1>0 0\n", text,
                      count=1, flags=re.MULTILINE)
    return text, _exact_euclidean


def _cvrp_problem_class():
    from tsplib95 import fields, models

    class CVRPProblem(models.StandardProblem):
        """StandardProblem plus the ``VEHICLES`` and ``DISTANCE`` (max route length) fields of CVRPLIB files."""

        vehicles = fields.IntegerField("VEHICLES")
        distance = fields.NumberField("DISTANCE")

    return CVRPProblem


def load_vrp_problem(problem_name, size="small"):
    """Load a bundled CVRP instance as a ``tsplib95`` problem.

    The problem also has ``vehicles`` and ``distance`` (max route length) when the file defines them.
    """
    tsplib95 = _import_tsplib95()
    text = _resource("vrp", size, f"{problem_name}.vrp").read_text()
    text, special = _normalize_vrp_text(text)
    return tsplib95.parse(text, problem_class=_cvrp_problem_class(), special=special)
