from .genome import Genome
import math
import random


class Population:
    def __init__(self, size, survival_rate):
        self.genomes = [
            Genome.create_default() for _ in range(size)
        ]
        self.survival_rate = survival_rate

    def run(self, eval_function, n):
        num_survivors = math.ceil(len(self.genomes) * self.survival_rate)
        for i in range(n):
            fitnesses = eval_function(self.genomes)
            print("gen: {} | max: {} | min: {} | avg: {}".format(
                i, max(fitnesses), min(fitnesses),
                sum(fitnesses) / len(self.genomes)))
            fitnesses = [(f, g) for f, g in zip(fitnesses, self.genomes)]
            fitnesses.sort(key=lambda t: t[0], reverse=True)
            survivors = [g for _, g in fitnesses[:num_survivors]]
            self.next_generation(survivors)

    def next_generation(self, survivors):
        new_genomes = [random.choice(survivors).copy() for _ in self.genomes]
        for g in new_genomes:
            g.mutate()
        self.genomes = new_genomes
