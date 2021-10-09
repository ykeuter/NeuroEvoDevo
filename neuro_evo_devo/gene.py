from .parameter import Parameter


class Gene:
    def __init__(self, parameters, rate, type):
        self.parameters = parameters
        self.rate = rate
        self.type = type

    def copy(self):
        parameters = {k: v.copy() for k, v in self.parameters.items()}
        return Gene(parameters, self.rate)

    def mutate(self):
        for v in self.parameters.values():
            v.mutate()

    @staticmethod
    def create_general_gene():
        parameters = {
            # gene selection
            "max_divisions": Parameter(min=0),
        }
        Gene(parameters, .0, "general")

    @staticmethod
    def create_cell_gene():
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
            # "xy_weight_std": Parameter(),
            # "xy_weight_weight": Parameter(),
            "xy_weight_width": Parameter(),
            # "z_weight_count": Parameter(),
            "z_weight_width": Parameter(),
            "xy_slope_inputs": Parameter(),
            "xy_slope_outputs": Parameter(),
            # neuron
            "neuron_bias": Parameter()
        }
        Gene(parameters, .001, "cell")
