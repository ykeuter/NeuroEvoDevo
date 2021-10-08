import math
import statistics

from .gene import CellGene


class Cell:
    def __init__(self, x, y, width_x, width_y, width_z,
                 inputs, outputs, genome):
        self.x = x
        self.y = y
        self.width_x = width_x
        self.width_y = width_y
        self.width_z = width_z
        self.inputs = inputs  # {cell: weight}
        self.outputs = outputs  # {cell: weight}
        self.genome = genome
        if genome is not None:
            self.active_gene = self.select_gene()
        else:
            self.active_gene = None

    def select_gene(self):
        self.active_gene = None
        best_score = -math.inf
        alpha, beta, gamma = self.get_greeks()
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

    def get_greeks(self):
        alpha, beta, gamma = 0, 0, 0
        for c, w in self.inputs.items():
            if c.active_gene is None:
                continue
            alpha += w * c.active_gene.parameters["alpha"]
            beta += w * c.active_gene.parameters["beta"]
            gamma += w * c.active_gene.parameters["gamma"]
        return alpha, beta, gamma

    def divide(self):
        p = self.active_gene.parameters
        # xs = [c.x for c in self.inputs.keys()]
        # ys = [c.y for c in self.inputs.keys()]
        x_score = (
            # statistics.pstdev(xs) * p["xy_weight_std"] +
            self.width_x * p["xy_weight_width"] +
            p["xy_bias"]
        )
        y_score = (
            # statistics.pstdev(ys) * p["xy_weight_std"] +
            self.width_y * p["xy_weight_width"] +
            p["xy_bias"]
        )
        z_score = (
            # len(self.inputs) * p["z_weight_count"] +
            self.width_z * p["z_weight_width"] +
            p["z_bias"]
        )
        max_score = max(x_score, y_score, z_score)
        if max_score < 0:
            return [self]
        if max_score == x_score:
            return self.divide_xy("x")
        if max_score == y_score:
            return self.divide_xy("y")
        return self.divide_z()

    def divide_z(self):
        new_cell = Cell(
            self.x, self.y, self.width_x, self.width_y, self.width_z / 2,
            {self: 1}, self.outputs, self.genome
        )
        self.width_z /= 2
        self.outputs = {new_cell: 1}
        for c in new_cell.outputs:
            c.inputs[new_cell] = c.inputs.pop(self)
        return [self, new_cell]

    def divide_xy(self, x_or_y):
        inputs1, inputs2 = self.split_io(x_or_y, "inputs")
        outputs1, outputs2 = self.split_io(x_or_y, "outputs")
        x1, y1, x2, y2, width_x, width_y = self.split_xy(x_or_y)
        cell1 = Cell(x1, y1, width_x, width_y, self.width_z,
                     inputs1, outputs1, self.genome)
        cell2 = Cell(x2, y2, width_x, width_y, self.width_z,
                     inputs2, outputs2, self.genome)
        self.update_refs(cell1, cell2)
        return [cell1, cell2]

    def update_refs(self, cell1, cell2):
        for c in self.inputs:
            c.outputs.pop(self)
        for c, v in cell1.inputs.items():
            c.outputs[cell1] = v
        for c, v in cell2.inputs.items():
            c.outputs[cell2] = v
        for c in self.outputs:
            c.inputs.pop(self)
        for c, v in cell1.outputs.items():
            c.inputs[cell1] = v
        for c, v in cell2.outputs.items():
            c.inputs[cell2] = v

    def split_io(self, x_or_y, in_or_out):
        slope = self.active_gene.parameters["xy_slope_" + in_or_out]
        io = getattr(self, in_or_out)
        xy = {c: getattr(c, x_or_y) for c in io}
        m = statistics.mean(xy.values())
        io1 = {c: max(0, min(1, (v - m) * slope + .5)) for c, v in xy.items()}
        io2 = {c: 1 - w for c, w in io1.items()}
        io1 = {c: w * io[c] for c, w in io1 if w != 0}
        io2 = {c: w * io[c] for c, w in io2 if w != 0}
        return io1, io2

    def split_xy(self, x_or_y):
        x1, y1, x2, y2, width_x, width_y = \
            self.x, self.y, self.x, self.y, self.width_x, self.width_y
        if x_or_y == "x":
            x1 = self.x - .5 * self.width_x
            x2 = self.x + .5 * self.width_x
            width_x = self.width_x / 2
        else:
            y1 = self.y - .5 * self.width_y
            y2 = self.y + .5 * self.width_y
            width_y = self.width_y / 2
        return x1, y1, x2, y2, width_x, width_y
