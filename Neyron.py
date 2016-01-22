import random
from math import pow

class Ney:
    def __init__(self):
        self._Inputs = [0 for i in range(100)]

    def transit_func(self):
        return sum(self._Inputs)


class MainNey(Ney):
    def __init__(self, newvalue):
        super().__init__()
        self.Value = newvalue
        self.Weights = [random.random() for i in range(100)]

    def correct_weight(self, koeff):
        for i in range(len(self.Weights)):
            self.Weights[i] += self._Inputs[i] * koeff

    def get_input(self, enterneys):
        for i in range(min(len(enterneys), len(self._Inputs))):
            enter = enterneys[i].transit_func()
            self._Inputs[i] = enter * self.Weights[i]


class EnterNey(Ney):
    def __init__(self, pic, back):
        super().__init__()
        k = 0
        for i in range(pic.size[0]):
            for j in range(pic.size[0]):
                self._Inputs[k] = sum(pic.getpixel((i, j))) / (sum(back) * pow(pic.size[0], 2))
                k += 1








