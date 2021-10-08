from cell import Cell
from collections import deque


class Phenotype:
    def __init__(self, input_coords, output_coords, genome):
        self.genome = genome
        egg = Cell(0, 0, 1, 1, 1, {}, {}, genome)
        self.inputs = [
            Cell(x, y, 0, 0, 0, {}, {egg: 1}, None) for x, y in input_coords
        ]
        self.outputs = [
            Cell(x, y, 0, 0, 0, {egg: 1}, {}, None) for x, y in output_coords
        ]
        egg.inputs = {c: 1 for c in self.inputs}
        egg.outputs = {c: 1 for c in self.outputs}
        self.develop(egg)
        return self

    def develop(self, egg):
        max_divisions = self.genome.genes[0].parameters["max_divisions"]
        num_divisions = 0
        idle = 0
        q = deque([egg])
        while num_divisions < max_divisions and idle < len(q):
            new_cells = q.popleft().divide()
            if len(new_cells) > 1:
                num_divisions += 1
                idle = 0
            else:
                idle += 1
            q.extend(new_cells)
