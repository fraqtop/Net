# -*- coding: utf-8 -*- #
from Net.Neyron import MainNey
from PIL import Image, ImageDraw, ImageFont
from random import randint


class Net:
    def get_random_colors(self, howmany, delta, pic_mode='RGBA'):
        cols = list()
        for i in range(howmany):
            if pic_mode == 'RGB':
                randcol = [randint(0, 255) for x in range(3)]
            else:
                randcol = [randint(0, 255) for x in range(4)]
            randcol = tuple(randcol)
            if self.out_of_range(randcol):
                cols.append(randcol)
        return cols

    @staticmethod
    def get_image(font_path):
        img = Image.new('RGBA', (500, 500), 'white')
        fnt = ImageFont.truetype(font_path, 60)
        draw = ImageDraw.Draw(img)
        for i in range(10):
            draw.text((int(i*40)+20, int(i*40)+20), str(i), 'black', fnt)
        return img

    def __init__(self, newdelta, newscale, newpixcount):
        self.__Neys = []
        self.__Neys = [MainNey(i) for i in range(10)]
        self.picsize = []
        self.__window = []
        self.back = tuple()
        self.delta = newdelta
        self.scale = newscale
        self.pixcount = newpixcount
        self.randcol = tuple()
        self.digits = []

    def out_of_range(self, col):
        if sum(self.back)-self.delta < sum(col) < sum(self.back)+self.delta:
            return False
        return True

    def cut_digits(self, pic):
        self.digits.clear()
        self.picsize = list(pic.size)
        cols = pic.getcolors()
        self.back = max(cols, key=lambda x: x[0])[1]
        self.randcol = self.get_random_colors(1, self.delta, pic.mode)[0]
        self.__window = [self.picsize[1], self.picsize[0], 0, 0]
        digits = []
        draft = pic.copy()
        draw = ImageDraw.Draw(draft)
        for j in range(self.scale, self.picsize[0]-self.scale, self.scale*2):
            for i in range(self.scale, self.picsize[1]-self.scale, self.scale*2):
                box = (j-self.scale, i-self.scale, j+self.scale, i+self.scale)
                if self.__is_outside(i, j) and self.__resp_area(box, draw, draft, pic):
                    digits.append((pic.crop(self.__window), self.__window))

                    # draft.show()

                    self.__window = [self.picsize[0], self.picsize[1], 0, 0]
        average = sum([x[0].size[0]*x[0].size[1] for x in digits])/len(digits)
        self.digits = [(x[0].resize((10, 10)), x[1]) for x in digits if x[0].size[0]*x[0].size[1] > average/3]

    def __resp_area(self, area, canvas, drf, pic):
        cols = pic.crop(area).getcolors()
        drcols = drf.crop(area).getcolors()
        if drcols[0][1] == tuple(self.randcol) or not self.__inside_pic(area):
            return False
        for i in cols:
            if i[0] > self.pixcount and self.out_of_range(i[1]):
                for j in range(2):
                    self.__window[j] = min((self.__window[j], area[j]))
                for j in range(2, 4, 1):
                    self.__window[j] = max((self.__window[j], area[j]))
                canvas.rectangle(area, self.randcol)
                self.__resp_area((area[0], area[1] - self.scale*2, area[2], area[3] - self.scale*2), canvas, drf, pic)
                self.__resp_area((area[0] + self.scale*2, area[1] - self.scale*2, area[2] + self.scale*2, area[3]-self.scale*2),
                                 canvas, drf, pic)
                self.__resp_area((area[0] + self.scale*2, area[1], area[2] + self.scale*2, area[3]), canvas, drf, pic)
                self.__resp_area((area[0] + self.scale*2, area[1] + self.scale*2, area[2] + self.scale*2, area[3]+self.scale*2),
                                 canvas, drf, pic)
                self.__resp_area((area[0], area[1] + self.scale*2, area[2], area[3]+self.scale*2), canvas, drf, pic)
                self.__resp_area((area[0] - self.scale*2, area[1] + self.scale*2, area[2] - self.scale*2, area[3]+self.scale*2),
                                 canvas, drf, pic)
                self.__resp_area((area[0] - self.scale*2, area[1], area[2] - self.scale*2, area[3]), canvas, drf, pic)
                self.__resp_area((area[0] - self.scale*2, area[1] - self.scale*2, area[2] - self.scale*2, area[3]-self.scale*2),
                                 canvas, drf, pic)
                return True
        return False

    def __is_outside(self, i, j):
        if self.__window[1] <= i <= self.__window[3] and self.__window[0] <= j <= self.__window[2]:
            return False
        return True

    def __inside_pic(self, box):
        if not 0 < box[0] < self.picsize[0]:
            return False
        if not 0 < box[1] < self.picsize[1]:
            return False
        if not 0 < box[2] < self.picsize[0]:
            return False
        if not 0 < box[3] < self.picsize[1]:
            return False
        return True

    def fill_network(self, digit):
        pic = self.digits[digit][0]
        pix = pic.load()
        for i in self.__Neys:
            for j in range(pic.size[0]):
                for k in range(pic.size[1]):
                    i.inputs[k+j*10] = abs(sum(self.back)-sum(pix[j, k]))
            i.process()
        return max(self.__Neys, key=lambda x: x.output).Value

    def paint_diagram(self):
        img = Image.new("RGB", (1000, 500), (255, 255, 255))
        self.back = (255, 255, 255)
        rndcls = self.get_random_colors(10, 10, 'RGB')
        draw = ImageDraw.Draw(img)
        box_for_pie = (400, 100, 600, 300)
        coconut = 1000/len(self.__Neys)
        input_sum = 0
        fnt = ImageFont.truetype('arialbi.ttf', 40)
        for i in self.__Neys:
            col = (int(coconut) * self.__Neys.index(i) + 20, 500 - int(i.output / 300),
                   int(coconut) * (self.__Neys.index(i) + 1) - 20, 500)
            draw.rectangle(col, rndcls[self.__Neys.index(i)])
            draw.text((round(col[0] + (col[2] - col[0]) / 2) - 10, 400), str(i.Value), (0, 0, 0), fnt)
            input_sum += i.output
        end_degree = 0
        for i in self.__Neys:
            draw.pieslice(box_for_pie, end_degree,
                          round(i.output * 360 / input_sum) + end_degree,
                          rndcls[self.__Neys.index(i)],
                          (0, 0, 0))
            end_degree += round(i.output * 360 / input_sum)
        return img

    def teach(self, correct):
        teaching_koeff = -0.005
        corr = list(filter(lambda x: x.Value == correct, self.__Neys))[0]
        corr.correct_weight(teaching_koeff*-1)
        corr = list(filter(lambda x: x.Value != correct, self.__Neys))
        map(lambda x: x.correct_weight(teaching_koeff), corr)

    def retneys(self):
        return self.__Neys

    def neuro_report(self, number):
        img = Image.new('RGB', (100, 100), 'white')
        draw = ImageDraw.ImageDraw(img)
        ney = self.__Neys[number]
        for i in range(10):
            for j in range(10):
                draw.rectangle((i*10, j*10, i*10+10, j*10+10), (int(ney.getweights()[i*10+j]*10), 0, 0))
        return img

    def force_teach(self, teaching_image):
        self.digits.clear()
        self.cut_digits(teaching_image)
        i = 1
        while i != 0:
            i = 0
            for j in range(len(self.__Neys)):
                self.fill_network(self.__Neys[j].Value)
                ans = max(self.__Neys, key=lambda x: x.output)
                print(ans.Value)
                if ans.Value != self.__Neys[j].Value:
                    i += 1
                    self.teach(j)
            print('_________')

    def save(self):
        f = open('w.txt', 'w')
        for i in self.__Neys:
            i.save(f)
        f.close()

    def load(self, path):
        f = open(path)
        for i in self.__Neys:
            w = f.readline()
            lst = w.split()
            i.get_wghts(lst)
