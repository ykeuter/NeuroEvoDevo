import random
import math


class Parameter:
    def __init__(self, mean=0, std=1, min=-math.inf, max=math.inf,
                 rate=.1, power=.01):
        self.value = random.gauss(mean, std)
        self.min = min
        self.max = max
        self.rate = rate
        self.power = power
        self.clamp()

    def clamp(self):
        self.value = max(min(self.value, self.max), self.min)

    def copy(self):
        return Parameter(
            self.value, 0, self.min, self.max, self.rate, self.power)

    def mutate(self):
        if random.random() < self.rate:
            self.value += random.gauss(0, self.power)
            self.clamp()
