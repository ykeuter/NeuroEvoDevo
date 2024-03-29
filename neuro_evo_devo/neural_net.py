import math


class NeuralNet:
    def __init__(self, phenotype):
        # work with cells, in layers
        # what abt bias in output?
        self.phenotype = phenotype
        self.eval_order = self.get_eval_order()

    def get_eval_order(self):
        ordered_cells = []
        processed_cells = set(self.phenotype.inputs)
        cells_in_line = set()
        cells_in_line.update(*(
            c.outputs.keys() for c in processed_cells
        ))
        while cells_in_line:
            new_cells_in_line = set()
            for c in cells_in_line:
                if all(i in processed_cells for i in c.inputs.keys()):
                    ordered_cells.append(c)
                    processed_cells.add(c)
                    new_cells_in_line.update(c.outputs.keys())
                else:
                    new_cells_in_line.add(c)
            cells_in_line = new_cells_in_line
        return ordered_cells

    def activate(self, input_values):
        values = {c: v for c, v in zip(self.phenotype.inputs, input_values)}
        for c in self.eval_order:
            s = sum(values[i] * w for i, w in c.inputs.items())
            if c.active_gene is not None:
                s += c.active_gene.parameters["neuron_bias"].value
            values[c] = math.tanh(s * 2.5)
        return [values[c] for c in self.phenotype.outputs]
