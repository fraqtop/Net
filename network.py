# -*- coding: utf-8 -*- #
from neuron import MainNeuron
from PIL import Image, ImageDraw, ImageFont
from random import randint


class Network:
    def get_random_colors(self, how_many, pic_mode='RGBA'):
        colors = list()
        for i in range(how_many):
            if pic_mode == 'RGB':
                random_color = [randint(0, 255) for x in range(3)]
            else:
                random_color = [randint(0, 255) for x in range(4)]
            random_color = tuple(random_color)
            if self.out_of_range(random_color):
                colors.append(random_color)
        return colors

    @staticmethod
    def get_image(font_path):
        image = Image.new('RGBA', (500, 500), 'white')
        font = ImageFont.truetype(font_path, 60)
        draw = ImageDraw.Draw(image)
        for i in range(10):
            draw.text((int(i*40)+20, int(i*40)+20), str(i), 'black', font)
        return image

    def __init__(self, new_delta, new_scale, new_pixel_count):
        self.__neurons = []
        self.__neurons = [MainNeuron(i) for i in range(10)]
        self.picture_size = []
        self.__window = []
        self.background = tuple()
        self.delta = new_delta
        self.scale = new_scale
        self.pixel_count = new_pixel_count
        self.random_color = tuple()
        self.digits = []

    def out_of_range(self, color):
        if sum(self.background)-self.delta < sum(color) < sum(self.background)+self.delta:
            return False
        return True

    def cut_digits(self, picture):
        self.digits.clear()
        self.picture_size = list(picture.size)
        colors = picture.getcolors()
        self.background = max(colors, key=lambda x: x[0])[1]
        self.random_color = self.get_random_colors(1, picture.mode)[0]
        self.__window = [self.picture_size[1], self.picture_size[0], 0, 0]
        digits = []
        draft = picture.copy()
        draw = ImageDraw.Draw(draft)
        for j in range(self.scale, self.picture_size[0] - self.scale, self.scale * 2):
            for i in range(self.scale, self.picture_size[1] - self.scale, self.scale * 2):
                box = (j-self.scale, i-self.scale, j+self.scale, i+self.scale)
                if self.__is_outside(i, j) and self.__resp_area(box, draw, draft, picture):
                    digits.append((picture.crop(self.__window), self.__window))

                    # draft.show()

                    self.__window = [self.picture_size[0], self.picture_size[1], 0, 0]
        average = sum([x[0].size[0]*x[0].size[1] for x in digits])/len(digits)
        self.digits = [(x[0].resize((10, 10)), x[1]) for x in digits if x[0].size[0]*x[0].size[1] > average/3]

    def __resp_area(self, area, canvas, draft, picture):
        picture_colors = picture.crop(area).getcolors()
        draft_colors = draft.crop(area).getcolors()
        if draft_colors[0][1] == tuple(self.random_color) or not self.__inside_pic(area):
            return False
        for i in picture_colors:
            if i[0] > self.pixel_count and self.out_of_range(i[1]):
                for j in range(2):
                    self.__window[j] = min((self.__window[j], area[j]))
                for j in range(2, 4, 1):
                    self.__window[j] = max((self.__window[j], area[j]))
                canvas.rectangle(area, self.random_color)
                self.__resp_area((area[0],
                                  area[1] - self.scale*2,
                                  area[2],
                                  area[3] - self.scale*2),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0] + self.scale*2,
                                  area[1] - self.scale*2,
                                  area[2] + self.scale*2,
                                  area[3]-self.scale*2),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0] + self.scale*2,
                                  area[1],
                                  area[2] + self.scale*2,
                                  area[3]),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0] + self.scale*2,
                                  area[1] + self.scale*2,
                                  area[2] + self.scale*2,
                                  area[3]+self.scale*2),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0],
                                  area[1] + self.scale*2,
                                  area[2],
                                  area[3]+self.scale*2),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0] - self.scale*2,
                                  area[1] + self.scale*2,
                                  area[2] - self.scale*2,
                                  area[3]+self.scale*2),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0] - self.scale*2,
                                  area[1],
                                  area[2] - self.scale*2,
                                  area[3]),
                                 canvas,
                                 draft,
                                 picture)
                self.__resp_area((area[0] - self.scale*2,
                                  area[1] - self.scale*2,
                                  area[2] - self.scale*2,
                                  area[3]-self.scale*2),
                                 canvas,
                                 draft,
                                 picture)
                return True
        return False

    def __is_outside(self, i, j):
        if self.__window[1] <= i <= self.__window[3] and self.__window[0] <= j <= self.__window[2]:
            return False
        return True

    def __inside_pic(self, box):
        if not 0 < box[0] < self.picture_size[0]:
            return False
        if not 0 < box[1] < self.picture_size[1]:
            return False
        if not 0 < box[2] < self.picture_size[0]:
            return False
        if not 0 < box[3] < self.picture_size[1]:
            return False
        return True

    def fill_network(self, digit):
        picture = self.digits[digit][0]
        pixel_map = picture.load()
        for i in self.__neurons:
            for j in range(picture.size[0]):
                for k in range(picture.size[1]):
                    i.inputs[k+j*10] = abs(sum(self.background) - sum(pixel_map[j, k]))
            i.process()
        return max(self.__neurons, key=lambda x: x.output).value

    def paint_diagram(self):
        img = Image.new("RGB", (1000, 500), (255, 255, 255))
        self.background = (255, 255, 255)
        random_colors = self.get_random_colors(10, 'RGB')
        draw = ImageDraw.Draw(img)
        box_for_pie = (400, 100, 600, 300)
        coconut = 1000/len(self.__neurons)
        input_sum = 0
        fnt = ImageFont.truetype('arialbi.ttf', 40)
        for i in self.__neurons:
            col = (int(coconut) * self.__neurons.index(i) + 20, 500 - int(i.output / 300),
                   int(coconut) * (self.__neurons.index(i) + 1) - 20, 500)
            draw.rectangle(col, random_colors[self.__neurons.index(i)])
            draw.text((round(col[0] + (col[2] - col[0]) / 2) - 10, 400), str(i.value), (0, 0, 0), fnt)
            input_sum += i.output
        end_degree = 0
        for i in self.__neurons:
            draw.pieslice(box_for_pie, end_degree,
                          round(i.output * 360 / input_sum) + end_degree,
                          random_colors[self.__neurons.index(i)],
                          (0, 0, 0))
            end_degree += round(i.output * 360 / input_sum)
        return img

    def teach(self, correct):
        teaching_rate = -0.005
        correct_neuron = list(filter(lambda x: x.value == correct, self.__neurons))[0]
        correct_neuron.correct_weight(teaching_rate*-1)
        correct_neuron = list(filter(lambda x: x.value != correct, self.__neurons))
        map(lambda x: x.correct_weight(teaching_rate), correct_neuron)

    def get_neurons(self):
        return self.__neurons

    def neuro_report(self, number):
        img = Image.new('RGB', (100, 100), 'white')
        draw = ImageDraw.ImageDraw(img)
        ney = self.__neurons[number]
        for i in range(10):
            for j in range(10):
                draw.rectangle((i*10, j*10, i*10+10, j*10+10), (int(ney.get_weights()[i*10+j]*10), 0, 0))
        return img

    def force_teach(self, teaching_image):
        self.digits.clear()
        self.cut_digits(teaching_image)
        errors_count = 1
        while errors_count != 0:
            errors_count = 0
            for j in range(len(self.__neurons)):
                self.fill_network(self.__neurons[j].value)
                answer = max(self.__neurons, key=lambda x: x.output)
                print(answer.value)
                if answer.value != self.__neurons[j].value:
                    errors_count += 1
                    self.teach(j)
            print('_________')

    def save_weights(self):
        f = open('w.txt', 'w')
        for i in self.__neurons:
            i.save(f)
        f.close()

    def load_weights(self, path):
        f = open(path)
        for i in self.__neurons:
            w = f.readline()
            loaded_weights = w.split()
            i.set_weights(loaded_weights)
