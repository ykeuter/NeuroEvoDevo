from parameter import Parameter


class Gene:
    def __init__(self, parameters, rate):
        self.parameters = parameters
        self.rate = rate
        return self

    def copy(self):
        parameters = {k: v.copy() for k, v in self.parameters.items()}
        return Gene(parameters, self.rate)

    def mutate(self):
        for v in self.parameters.values():
            v.mutate()

    @staticmethod
    def create_cell_type_gene():
        parameters = {
            # gene selection
            "alpha": Parameter(),
            "beta": Parameter(),
            "gamma": Parameter(),
            "weight_alpha": Parameter(),
            "weight_beta": Parameter(),
            "weight_gamma": Parameter(),
            "gene_bias": Parameter(),
            # split
            "xy_bias": Parameter(),
            "z_bias": Parameter(),
            "xy_weight": Parameter(),
            "z_weight": Parameter(),
            "xy_slope": Parameter(),
            # neuron
            "neuron_bias": Parameter()
        }
        return Gene(parameters, .001)

    @staticmethod
    def create_general_gene():
        parameters = {
            # gene selection
            "max_divisions": Parameter(min=0),
        }
        return Gene(parameters, 0)
