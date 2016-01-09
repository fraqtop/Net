import random


class Ney:
    def __init__(self, newvalue):
        self.Matrix = [[random.random() for x in range(100)] for x in range(100)]
        self.Value = newvalue