import ast
import math
import os
import tempfile
from unittest import TestCase

from pyevolve.planning import (
    get_distance_matrixes_from_tsp_problem,
    list_tsp_problems,
    list_vrp_problems,
    load_cvrp_instance,
    load_tsp_problem,
    load_vrp_problem,
    make_cvrp_fitness,
    run_tsp,
    tsp_file_list_all,
)
from pyevolve.representations import G1DList
from pyevolve.selections.Selectors import GTournamentSelector


class PlanningDatasetsTestCase(TestCase):
    def test_bundled_tsp_list_matches_known_problems(self):
        self.assertEqual(sorted(tsp_file_list_all), list_tsp_problems())

    def test_every_bundled_tsp_loads(self):
        for name in list_tsp_problems():
            with self.subTest(name=name):
                problem = load_tsp_problem(name)
                self.assertGreater(len(list(problem.get_nodes())), 0)

    def test_every_bundled_vrp_loads(self):
        for size in ("small", "big"):
            names = list_vrp_problems(size)
            self.assertGreater(len(names), 0)
            for name in names:
                with self.subTest(size=size, name=name):
                    problem = load_vrp_problem(name, size)
                    self.assertIsNotNone(problem.capacity)
                    self.assertEqual(problem.dimension, len(list(problem.get_nodes())))
                    self.assertEqual(problem.dimension, len(problem.demands))
                    self.assertEqual(len(problem.depots), 1)
                    self.assertEqual(problem.demands[problem.depots[0]], 0)

    def test_golden_vrp_depot_coordinates_and_exact_distances(self):
        # Golden_* / Li_* give the depot as coordinates and use unrounded Euclidean distances
        problem = load_vrp_problem("Golden_9", "big")
        self.assertEqual(problem.depots, [0])
        self.assertEqual(list(problem.node_coords[0]), [0.0, -15.0])
        self.assertEqual(problem.capacity, 1000)
        self.assertEqual(problem.vehicles, 14)
        self.assertAlmostEqual(problem.get_weight(0, 1), math.sqrt(2))

    def test_missing_dataset_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_tsp_problem("does_not_exist")


class PlanningTspDistanceMatrixTestCase(TestCase):
    def test_matrix_is_indexed_from_zero_for_one_based_instances(self):
        # att48 numbers its nodes 1..48, br17 numbers them 0..16
        for name in ("att48", "bayg29", "br17"):
            with self.subTest(name=name):
                problem = load_tsp_problem(name)
                nodes = list(problem.get_nodes())
                matrix_dict, matrix_list = get_distance_matrixes_from_tsp_problem(name)
                self.assertEqual(len(matrix_list), len(nodes))
                self.assertEqual(matrix_list[0][1], problem.get_weight(nodes[0], nodes[1]))
                self.assertEqual(matrix_dict[0, len(nodes) - 1], problem.get_weight(nodes[0], nodes[-1]))


class PlanningCVRPTestCase(TestCase):
    def test_load_cvrp_instance_and_fitness(self):
        instance = load_cvrp_instance("A-n33-k5")
        self.assertEqual(instance.node_count, 33)
        self.assertEqual(len(instance.customers), 32)
        self.assertNotIn(instance.depot_index, instance.customers)

        chromosome = G1DList.G1DList(len(instance.customers))
        chromosome.setInternalList(list(instance.customers))
        self.assertGreater(make_cvrp_fitness(instance)(chromosome), 0)

    def test_load_cvrp_instance_with_depot_coordinates(self):
        instance = load_cvrp_instance("Golden_1", "big")
        self.assertEqual(instance.node_count, 241)
        self.assertEqual(instance.demands[instance.depot_index], 0)
        self.assertEqual(len(instance.customers), 240)


class PlanningRunTspTestCase(TestCase):
    def test_run_tsp_writes_log_to_cwd_experiments(self):
        # eil51 uses coordinates, br17 a 0-based explicit matrix, att48 1-based ATT distances
        for problem_name in ("eil51", "br17", "att48"):
            with self.subTest(problem_name=problem_name):
                old_cwd = os.getcwd()
                with tempfile.TemporaryDirectory() as tmp:
                    os.chdir(tmp)
                    try:
                        run_tsp(problem_name, max_generation_count=2, population_size=10, freq_stats=0)
                        logs = os.listdir(os.path.join(tmp, "experiments"))
                    finally:
                        os.chdir(old_cwd)
                self.assertEqual(len(logs), 1)
                self.assertTrue(logs[0].endswith(".txt"))

    def _run_in_tmp(self, **kwargs):
        """Run ``run_tsp("br17", ...)`` in a temporary cwd; return ``{log file name: parsed entries}``."""
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                run_tsp("br17", max_generation_count=2, population_size=10, freq_stats=0, **kwargs)
                log_dir = os.path.join(tmp, "experiments")
                logs = {}
                for name in os.listdir(log_dir) if os.path.isdir(log_dir) else []:
                    with open(os.path.join(log_dir, name)) as file:
                        logs[name] = dict(line.rstrip("\n").split(": ", 1) for line in file)
                return logs
            finally:
                os.chdir(old_cwd)

    def test_run_tsp_log_content(self):
        logs = self._run_in_tmp(mutation_rate=0.05, selection_method=GTournamentSelector)
        self.assertEqual(len(logs), 1)
        entries = next(iter(logs.values()))

        self.assertEqual(list(entries), [
            "experiment_name", "experiment_duration", "max_generation_count", "population_size",
            "crossover_method", "crossover_rate", "mutation_method", "mutation_rate",
            "selection_method", "initialization_method", "raw_score", "fitness", "tour",
        ])
        self.assertEqual(entries["max_generation_count"], "2")
        self.assertEqual(entries["population_size"], "10")
        self.assertEqual(entries["crossover_rate"], "1.0")
        self.assertEqual(entries["mutation_rate"], "0.05")
        # Operators are logged by name, defaults included (no slot dumps or memory addresses)
        self.assertEqual(entries["crossover_method"], "G1DListCrossoverEdge")
        self.assertEqual(entries["mutation_method"], "G1DListMutatorSwap")
        self.assertEqual(entries["selection_method"], "GTournamentSelector")
        self.assertEqual(entries["initialization_method"], "G1DListTSPInitializatorRandom")
        self.assertGreater(float(entries["raw_score"]), 0)
        self.assertEqual(sorted(ast.literal_eval(entries["tour"])), list(range(17)))

    def test_run_tsp_log_experiments_false_writes_no_log(self):
        self.assertEqual(self._run_in_tmp(log_experiments=False), {})
