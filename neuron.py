import random


class Neuron:
    def __init__(self):
        self.output = 0
        self.inputs = [random.random() for i in range(100)]


class MainNeuron(Neuron):
    def __init__(self, new_value):
        super().__init__()
        self.value = new_value
        self.__weights = [random.random() for i in range(100)]

    def correct_weight(self, k):
        for i in range(len(self.__weights)):
            self.__weights[i] += self.inputs[i] * k

    def process(self):
        self.output = 0
        for i in range(len(self.__weights)):
            self.output += float(self.inputs[i] * self.__weights[i])

    def save(self, file_stream):
        for i in self.__weights:
            file_stream.write(str(i)+' ')
        file_stream.write('\n')

    def get_weights(self):
        return self.__weights

    def set_weights(self, weights):
        for i in range(len(weights)):
            self.__weights[i] = float(weights[i])
