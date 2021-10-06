import math

from gene import CellGene


class Cell:
    def __init__(self, x, y, inputs, weights, outputs, genome):
        self.x = x
        self.y = y
        self.inputs = inputs
        self.weights = weights
        self.outputs = outputs
        self.genome = genome
        if genome is not None:
            self.active_gene = self.select_gene()
        else:
            self.active_gene = None
        return self

    def select_gene(self):
        self.active_gene = None
        best_score = -math.inf
        alpha, beta, gamma = 0, 0, 0
        for w, c in zip(self.weights, self.inputs):
            if c.active_gene is None:
                continue
            alpha += w * c.active_gene.parameters["alpha"]
            beta += w * c.active_gene.parameters["beta"]
            gamma += w * c.active_gene.parameters["gamma"]
        for g in self.genome.genes:
            if not isinstance(g, CellGene):
                continue
            score = (
                g.parameters["weight_alpha"] * alpha +
                g.parameters["weight_beta"] * beta +
                g.parameters["weight_gamma"] * gamma +
                g.parameters["gene_bias"]
            )
            if score > best_score:
                best_score = score
                self.active_gene = g

    def divide(self):
        pass
