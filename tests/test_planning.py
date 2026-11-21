import os
import tempfile
from unittest import TestCase

from pyevolve.planning import (
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


class PlanningDatasetsTestCase(TestCase):
    def test_bundled_tsp_list_matches_known_problems(self):
        self.assertEqual(sorted(tsp_file_list_all), list_tsp_problems())

    def test_every_bundled_tsp_loads(self):
        for name in list_tsp_problems():
            with self.subTest(name=name):
                problem = load_tsp_problem(name)
                self.assertGreater(len(list(problem.get_nodes())), 0)

    def test_every_bundled_vrp_loads(self):
        # The Golden_* and Li_* instances have VEHICLES/DISTANCE header fields that tsplib95 0.7.1 cannot parse.
        unparseable_prefixes = ("Golden_", "Li_")
        for size in ("small", "big"):
            names = list_vrp_problems(size)
            self.assertGreater(len(names), 0)
            for name in names:
                if name.startswith(unparseable_prefixes):
                    continue
                with self.subTest(size=size, name=name):
                    self.assertIsNotNone(load_vrp_problem(name, size).capacity)

    def test_missing_dataset_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_tsp_problem("does_not_exist")


class PlanningCVRPTestCase(TestCase):
    def test_load_cvrp_instance_and_fitness(self):
        instance = load_cvrp_instance("A-n33-k5")
        self.assertEqual(instance.node_count, 33)
        self.assertEqual(len(instance.customers), 32)
        self.assertNotIn(instance.depot_index, instance.customers)

        chromosome = G1DList.G1DList(len(instance.customers))
        chromosome.setInternalList(list(instance.customers))
        self.assertGreater(make_cvrp_fitness(instance)(chromosome), 0)


class PlanningRunTspTestCase(TestCase):
    def test_run_tsp_writes_log_to_cwd_experiments(self):
        # eil51 uses coordinates, br17 an explicit distance matrix
        for problem_name in ("eil51", "br17"):
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
