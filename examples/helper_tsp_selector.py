import argparse
import math
import os
import random
import time
from itertools import combinations

import numpy as np
import skfuzzy as fuzz
from scipy.stats import entropy
from skfuzzy import control as ctrl

from pyevolve import Consts
from pyevolve import GSimpleGA
from pyevolve.initializations.InitializationPermutations import G1DListTSPInitializatorRandom
from pyevolve.perturbations.MutatorG1DListPermutations import G1DListMutatorDisplacement
from pyevolve.representations import G1DList
from pyevolve.selections.SelectionRank import (
    SelectorExponentialRanking,
    SelectorExplorationExploitationBalance,
    SelectorFitnessProportional,
    SelectorLinearRanking,
    SelectorNewTournament,
    SelectorSplitRanking,
)
from pyevolve.selections.Selectors import GTournamentSelector


dict_selector_operators = {
    "FPS": SelectorFitnessProportional,
    "LRS": SelectorLinearRanking,
    "ERS": SelectorExponentialRanking,
    "EEBS": SelectorExplorationExploitationBalance,
    "SRS": SelectorSplitRanking,
    "NTS": SelectorNewTournament,
    "TS": GTournamentSelector,
}

try:
    from helper_tsp import PIL_SUPPORT, write_tour_to_img
except ImportError:
    PIL_SUPPORT = False
    write_tour_to_img = None


def _build_control_system():
    diversity = ctrl.Antecedent(np.linspace(0, 1, 101), "diversity")
    iteration = ctrl.Antecedent(np.linspace(0, 1, 101), "iteration")
    alpha = ctrl.Consequent(np.linspace(0, 1, 101), "alpha")

    for variable, labels in (
        (diversity, ("H", "HM", "M", "LM", "L")),
        (iteration, ("L", "LM", "M", "HM", "H")),
        (alpha, ("L", "LM", "M", "HM", "H")),
    ):
        for index, label in enumerate(labels):
            left = max(0.0, (index - 1) / 4)
            center = index / 4
            right = min(1.0, (index + 1) / 4)
            variable[label] = fuzz.trimf(variable.universe, [left, center, right])

    outputs = {
        "L": ("M", "M", "HM", "H", "H"),
        "LM": ("M", "M", "M", "HM", "H"),
        "M": ("LM", "M", "M", "M", "HM"),
        "HM": ("L", "LM", "M", "M", "M"),
        "H": ("L", "L", "LM", "M", "M"),
    }
    rules = []
    for diversity_label, output_labels in outputs.items():
        for iteration_label, output_label in zip(
            ("L", "LM", "M", "HM", "H"), output_labels
        ):
            rules.append(
                ctrl.Rule(
                    diversity[diversity_label] & iteration[iteration_label],
                    alpha[output_label],
                )
            )

    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))


class SelectorController:
    def __init__(self, strategy="deterministic", max_iterations=1001):
        self.strategy = strategy
        self.max_iterations = max_iterations
        self.selection_sim = _build_control_system()
        self.q_table = np.zeros((5, 5, 5))
        self.prev_state = (0, 0)
        self.prev_action = 2
        self.alpha_bins = [0.1, 0.3, 0.5, 0.7, 0.9]
        self.rewards = [0.0] * len(self.alpha_bins)
        self.counts = [0] * len(self.alpha_bins)
        self.alpha_history = []
        self.last_score = -1

    @staticmethod
    def population_diversity(population):
        if len(population) < 2:
            return 0.0

        distances = [
            sum(gene1 != gene2 for gene1, gene2 in zip(first.genomeList, second.genomeList))
            for first, second in combinations(population, 2)
        ]
        minimum = min(distances)
        maximum = max(distances)
        if maximum == minimum:
            return 0.0
        normalized = (sum(distances) / len(distances) - minimum) / (maximum - minimum) 
        return normalized

    def calculate_alpha(self, iteration, population, best):
        if self.strategy == "deterministic":
            return 0.1 + 0.8 * (iteration / self.max_iterations)

        if self.strategy == "fuzzy":
            diversity_score = self.population_diversity(population) or 1.0
            self.selection_sim.input["diversity"] = 1 - diversity_score
            self.selection_sim.input["iteration"] = iteration / self.max_iterations
            self.selection_sim.compute()
            return self.selection_sim.output["alpha"]

        if self.strategy == "entropy":
            matrix = np.array([individual.genomeList for individual in population])
            entropies = [
                entropy(np.unique(matrix[:, index], return_counts=True)[1], base=2)
                for index in range(matrix.shape[1])
            ]
            return max(0.1, min(1.0, np.mean(entropies)))

        if self.strategy == "adaptive":
            if iteration == 0:
                self.alpha_history = [0.5]
                return 0.5
            improvement = (self.last_score - best.getRawScore()) / 1000.0
            delta = max(-0.05, min(0.05, improvement))
            previous = self.alpha_history[-1]
            new_alpha = 0.9 * previous + 0.1 * (previous + delta)
            new_alpha = min(1.0, max(0.0, new_alpha))
            self.alpha_history.append(new_alpha)
            return new_alpha

        if self.strategy == "selfadaptive":
            return np.mean([getattr(individual, "alpha", 0.5) for individual in population])

        if self.strategy == "qlearning":
            diversity_bin = int((1 - self.population_diversity(population)) * 4)
            iteration_bin = int((iteration / self.max_iterations) * 4)
            if random.random() < 0.1:
                action = random.randint(0, 4)
            else:
                action = np.argmax(self.q_table[diversity_bin, iteration_bin])

            reward = 0 if self.last_score < 0 else max(
                0.0,
                (self.last_score - best.getRawScore()) / max(1.0, abs(self.last_score)),
            )
            old_value = self.q_table[self.prev_state[0], self.prev_state[1], self.prev_action]
            self.q_table[self.prev_state[0], self.prev_state[1], self.prev_action] = old_value + 0.1 * (
                reward + 0.9 * np.max(self.q_table[diversity_bin, iteration_bin]) - old_value
            )
            self.prev_state = (diversity_bin, iteration_bin)
            self.prev_action = action
            return self.alpha_bins[action]

        if self.strategy == "bandit":
            for index, count in enumerate(self.counts):
                if count == 0:
                    self.counts[index] += 1
                    return self.alpha_bins[index]

            total = sum(self.counts)
            values = [
                self.rewards[index] / self.counts[index]
                + math.sqrt(2 * math.log(total) / self.counts[index])
                for index in range(len(self.alpha_bins))
            ]
            index = np.argmax(values)
            reward = max(-10, min(1000, self.last_score - best.getRawScore()))
            self.rewards[index] += reward
            self.counts[index] += 1
            if iteration == self.max_iterations - 1:
                self.rewards = [0.0] * len(self.alpha_bins)
                self.counts = [0] * len(self.alpha_bins)
            return self.alpha_bins[index]

        return 0.5

    def callback(self, log_file, results_directory):
        def evolve_callback(ga_engine):
            current_generation = ga_engine.getCurrentGeneration()
            os.makedirs(results_directory, exist_ok=True)
            best = ga_engine.bestIndividual()
            alpha = self.calculate_alpha(current_generation, ga_engine.internalPop, best)

            if alpha < 0.7:
                ga_engine.selector.set(dict_selector_operators["EEBS"])
            elif alpha < 0.8:
                ga_engine.selector.set(dict_selector_operators["NTS"])
            elif alpha < 1:
                ga_engine.selector.set(dict_selector_operators["FPS"])

            log_file.write(str(best.getRawScore()) + "\n")
            self.last_score = best.getRawScore()
            return False

        return evolve_callback


def mutate_alpha(individual, sigma=0.05):
    individual.alpha = max(0.0, min(1.0, getattr(individual, "alpha", 0.5) + random.gauss(0, sigma)))


def self_adaptive_mutator(genome, **args):
    G1DListMutatorDisplacement(genome, **args)
    mutate_alpha(genome)
    return 1


def run_selector_ga(
    crossover_operator_func,
    distance_matrix,
    city_count,
    log_file,
    strategy,
    generation_count=1001,
    results_directory="tspimg",
    coordinates=None,
    save_images=False,
    evaluator=None,
    genome_values=None,
):
    controller = SelectorController(strategy, generation_count)
    genome_size = len(genome_values) if genome_values is not None else city_count
    genome = G1DList.G1DList(genome_size)
    genome.setParams(dist=distance_matrix)
    if evaluator is None:
        evaluator = lambda chromosome: tour_length(distance_matrix, chromosome, city_count)
    genome.evaluator.set(evaluator)
    genome.crossover.set(crossover_operator_func)
    genome.mutator.set(G1DListMutatorDisplacement)
    if genome_values is None:
        genome.initializator.set(G1DListTSPInitializatorRandom)
    else:
        def initialize_genome(custom_genome, **args):
            values = list(genome_values)
            random.shuffle(values)
            custom_genome.setInternalList(values)

        genome.initializator.set(initialize_genome)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(generation_count)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)
    ga.setPopulationSize(80)
    ga.selector.set(dict_selector_operators["EEBS"])
    ga.stepCallback.set(controller.callback(log_file, results_directory))
    start = time.time()
    ga.evolve(freq_stats=1)
    log_file.write(str(time.time() - start) + "\n")

    if save_images and PIL_SUPPORT and coordinates is not None:
        image_file = os.path.join(results_directory, "tsp_result.png")
        write_tour_to_img(coordinates, ga.bestIndividual(), image_file, generation_count)


def tour_length(matrix, tour, city_count):
    total = 0
    genome = tour.getInternalList()
    for index in range(city_count):
        total += matrix[genome[index], genome[(index + 1) % city_count]]
    return total


def run_experiment_series(main_run, crossover_methods, crossover_operators, default_problem, strategy,
                          include_strategy_in_filename=True):
    for crossover_operator_name in crossover_methods:
        randomseed = 1000
        for _ in range(1, 31):
            parser = argparse.ArgumentParser(description="crossover, tsp problems")
            parser.add_argument("--crossover", default=crossover_operator_name)
            parser.add_argument("--problemname", default=default_problem)
            randomseed += 1
            parser.add_argument("--randomseed", default=randomseed, type=int)
            args = parser.parse_args()
            random.seed(args.randomseed)
            if args.crossover not in crossover_operators:
                raise ValueError(args.crossover + " is not in dict_crossoever_operators")

            print(args)
            suffix = "_" + strategy if include_strategy_in_filename else ""
            filename = f"examples/experiments/{args.crossover}_{args.problemname}_Experiment_{args.randomseed}{suffix}.txt"
            with open(filename, "w") as log_file:
                main_run(crossover_operators[args.crossover], args.problemname, log_file)