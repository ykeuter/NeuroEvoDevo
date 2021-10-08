import math


class NeuralNet:
    def __init__(self, phenotype):
        # work with cells, in layers
        # what abt bias in output?
        self.phenotype = phenotype
        self.eval_order = self.get_eval_order()
        return self

    def get_eval_order(self):
        ordered_cells = []
        cells_in_line = set()
        cells_in_line.update(c.outputs.keys() for c in self.phenotype.inputs)
        while cells_in_line:
            new_cells_in_line = set()
            for c in cells_in_line:
                if all(i in ordered_cells for i in c.inputs.keys()):
                    ordered_cells.append(c)
                    new_cells_in_line.update(c.outputs.keys())
                else:
                    new_cells_in_line.add(c)
            cells_in_line = new_cells_in_line
        return ordered_cells

    def activate(self, input_values):
        values = {c: v for c, v in zip(self.phenotype.inputs, input_values)}
        for c in self.eval_order:
            values[c] = math.tanh(
                sum(
                    values[i] * w for i, w in c.inputs.items()
                ) * 2.5
            )
        return [values[c] for c in self.phenotype.outputs]
