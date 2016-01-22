# -*- coding: utf-8 -*- #
from Net.Neyron import EnterNey, MainNey
from PIL import Image, ImageDraw, ImageFont


class Net:
    def __init__(self, newpic, newdelta, newscale, newpixcount, newrandcol):
        self.__Neys = []
        self.EntryNeys = []
        for i in range(10):
            self.__Neys.append(MainNey(i))
        if isinstance(newpic, Image.Image):
            self.picsize = (newpic.size[0], newpic.size[1])
            self.picture = newpic
            self.__window = [self.picsize[1], self.picsize[0], 0, 0]
            self.__draw = ImageDraw.Draw(self.picture)
            self.__back = max(newpic.getcolors())[1]
            self.delta = newdelta
            self.scale = newscale
            self.pixcount = newpixcount
            self.randcol = newrandcol
            self.digits = self.cut_digits()

    def out_of_range(self, col):
        if sum(self.__back)-self.delta < sum(col) < sum(self.__back)+self.delta:
            return False
        return True

    def cut_digits(self):
        digits = []
        draft = self.picture.copy()
        draw = ImageDraw.Draw(draft)
        for j in range(self.scale, self.picsize[0]-self.scale, self.scale):
            for i in range(self.scale, self.picsize[1]-self.scale, self.scale):
                box = (j-self.scale, i-self.scale, j+self.scale, i+self.scale)
                if self.__is_outside(i, j) and self.__resp_area(box, draw, draft):
                    digits.append((self.picture.crop(self.__window).resize((100, 100)), self.__window))
                    self.__window = [self.picsize[0], self.picsize[1], 0, 0]
        return digits

    def __resp_area(self, area, canvas, drf):
        cols = self.picture.crop(area).getcolors()
        drcols = drf.crop(area).getcolors()
        if len(drcols) == 1 and drcols[0][1] == tuple(self.randcol) or not self.__inside_pic(area):
            return False
        for i in cols:
            if i[0] > self.pixcount and self.out_of_range(i[1]):
                for j in range(2):
                    self.__window[j] = min((self.__window[j], area[j]))
                for j in range(2, 4, 1):
                    self.__window[j] = max((self.__window[j], area[j]))
                canvas.rectangle(area, self.randcol)
                self.__resp_area((area[0], area[1] - self.scale, area[2], area[3]-self.scale), canvas, drf)
                self.__resp_area((area[0] + self.scale, area[1], area[2] + self.scale, area[3]), canvas, drf)
                self.__resp_area((area[0], area[1] + self.scale, area[2], area[3]+self.scale), canvas, drf)
                self.__resp_area((area[0] - self.scale, area[1], area[2] - self.scale, area[3]), canvas, drf)
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
        self.EntryNeys.clear()
        step = int(self.digits[digit][0].size[0] * 0.1)
        for i in range(0, self.digits[digit][0].size[0], step):
            for j in range(0, self.digits[digit][0].size[0], step):
                self.EntryNeys.append(EnterNey(self.digits[digit][0].crop((j, i, j+step, i+step)), self.__back))
        for i in self.__Neys:
            i.get_input(self.EntryNeys)

    def activate(self, func):
        if func() < 40:
            return 0
        return func()

    def paint_diagram(self, rndcls):
        img = Image.new("RGB", (1000, 500), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        box_for_pie = (400, 100, 600, 300)
        coconut = 1000/len(self.__Neys)
        input_sum = 0
        fnt = ImageFont.truetype('arialbi.ttf', 40)
        for i in self.__Neys:
            col = (int(coconut) * self.__Neys.index(i)+20, 500 - int(self.activate(i.transit_func)) * 2,
                   int(coconut) * (self.__Neys.index(i)+1)-20, 500)
            draw.rectangle(col, rndcls[self.__Neys.index(i)])
            draw.text((round(col[0] + (col[2] - col[0]) / 2) - 10, col[1] + (col[3] - col[1])/2), str(i.Value), (0, 0, 0), fnt)
            input_sum += self.activate(i.transit_func)
        end_degree = 0
        for i in self.__Neys:
            draw.pieslice(box_for_pie, end_degree,
                          round(self.activate(i.transit_func) * 360 / input_sum)+end_degree,
                          rndcls[self.__Neys.index(i)],
                          (0, 0, 0))
            end_degree += round(self.activate(i.transit_func) * 360 / input_sum)
        return img

    def teach(self, right):
        teaching_koeff = -0.1
        for i in self.__Neys:
            if i.Value == int(right):
                i.correct_weight(teaching_koeff * -1)
            else:
                i.correct_weight(teaching_koeff)

    def decide(self):
        result = [0, 0]
        for i in self.__Neys:
            if self.activate(i.transit_func) > result[1]:
                result[0] = i.Value
                result[1] = i.transit_func()
        return result[0]

# from random import randint
#
# def getcolors(number=1):
#     while number != 1:
#         result = getcolors(number - 1)
#         number = 1
#     rcol = [randint(0, 255) for x in range(3)]
#     rcol.append(255)
#     try:
#         while len([x for x in result if abs(x[0] - rcol[0]) + abs(x[1] - rcol[1]) + abs(x[2] - rcol[2]) < 200]) != 0:
#             rcol = [randint(0, 255) for x in range(3)]
#             rcol.append(255)
#         result.append(tuple(rcol))
#     except:
#         result = []
#         result.append(tuple(rcol))
#     return result

# p = Image.open('qwe.png')
# n = Net(p, 40, 20, 80, (183, 111, 11, 255))
# n.fill_network(0)
# print(n.decide())