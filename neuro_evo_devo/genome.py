import random
from gene import GeneralGene, CellGene


class Genome:
    def __init__(self, genes):
        self.genes = genes

    def copy(self):
        genes = [g.copy() for g in self.genes]
        return Genome(genes)

    def mutate(self):
        new_genes = []
        for g in self.genes:
            if random.random() < g.rate:
                extra_gene = g.copy()
                extra_gene.mutate()
                new_genes.append(extra_gene)
            g.mutate()
            new_genes.append(g)

    @staticmethod
    def create_default():
        genes = [GeneralGene(), CellGene()]
        return Genome(genes)
