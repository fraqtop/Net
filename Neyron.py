import random


class Ney:
    def __init__(self):
        self.output = 0
        self.inputs = [random.random() for i in range(100)]


class MainNey(Ney):
    def __init__(self, newvalue):
        super().__init__()
        self.Value = newvalue
        self.__weights = [random.random() for i in range(100)]

    def correct_weight(self, koeff):
        for i in range(len(self.__weights)):
            self.__weights[i] += self.inputs[i] * koeff

    def process(self):
        self.output = 0
        for i in range(len(self.__weights)):
            self.output += float(self.inputs[i] * self.__weights[i])

    def save(self, fstream):
        for i in self.__weights:
            fstream.write(str(i)+' ')
        fstream.write('\n')

    def getweights(self):
        return self.__weights

    def get_wghts(self, wght_lst):
        for i in range(len(wght_lst)):
            self.__weights[i] = float(wght_lst[i])