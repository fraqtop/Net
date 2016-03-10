# -*- coding: utf-8 -*- #
from Net.Neyron import EnterNey, MainNey
from PIL import Image, ImageDraw, ImageFont


class Net:
    @staticmethod
    def get_image():
        img = Image.new('RGBA', (500, 500), 'white')
        fnt = ImageFont.truetype('BRADHITC.TTF', 60)
        draw = ImageDraw.Draw(img)
        for i in range(10):
            draw.text((int(i*40)+20, int(i*40)+20), str(i), 'black', fnt)
        return img

    def __init__(self, newdelta, newscale, newpixcount, newrandcol):
        self.__Neys = []
        self.EntryNeys = []
        for i in range(10):
            self.__Neys.append(MainNey(i))
        self.picsize = []
        self.__window = []
        self.back = tuple
        self.delta = newdelta
        self.scale = newscale
        self.pixcount = newpixcount
        self.randcol = newrandcol
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
        self.__window = [self.picsize[1], self.picsize[0], 0, 0]
        digits = []
        draft = pic.copy()
        draw = ImageDraw.Draw(draft)
        for j in range(self.scale, self.picsize[0]-self.scale, self.scale):
            for i in range(self.scale, self.picsize[1]-self.scale, self.scale):
                box = (j-self.scale, i-self.scale, j+self.scale, i+self.scale)
                if self.__is_outside(i, j) and self.__resp_area(box, draw, draft, pic):
                    digits.append((pic.crop(self.__window), self.__window))

                    # draft.show()

                    self.__window = [self.picsize[0], self.picsize[1], 0, 0]
        average = sum([x[0].size[0]*x[0].size[1] for x in digits])/len(digits)
        self.digits = [(x[0].resize((100, 100)), x[1]) for x in digits if x[0].size[0]*x[0].size[1]>average/1.5]

    def __resp_area(self, area, canvas, drf, pic):
        cols = pic.crop(area).getcolors()
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
                self.__resp_area((area[0], area[1] - self.scale, area[2], area[3]-self.scale), canvas, drf, pic)
                self.__resp_area((area[0] + self.scale, area[1], area[2] + self.scale, area[3]), canvas, drf, pic)
                self.__resp_area((area[0], area[1] + self.scale, area[2], area[3]+self.scale), canvas, drf, pic)
                self.__resp_area((area[0] - self.scale, area[1], area[2] - self.scale, area[3]), canvas, drf, pic)
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
                self.EntryNeys.append(EnterNey(self.digits[digit][0].crop((j, i, j+step, i+step)), self.back))
        for i in self.__Neys:
            i.get_input(self.EntryNeys)
        return self.digits[digit][1]

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
            col = (int(coconut) * self.__Neys.index(i)+20, 500 - int(self.activate(i.transit_func)/2),
                   int(coconut) * (self.__Neys.index(i)+1)-20, 500)
            draw.rectangle(col, rndcls[self.__Neys.index(i)])
            draw.text((round(col[0] + (col[2] - col[0]) / 2) - 10, 400), str(i.Value), (0, 0, 0), fnt)
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
        teaching_koeff = -0.005
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
                result[1] = round(i.transit_func())
        return result

    def retneys(self):
        return self.__Neys

    def force_teach(self):
        self.digits.clear()
        img = Net.get_image()
        self.cut_digits(img)
        i = 1
        while i != 0:
            i = 0
            for j in range(int(len(self.__Neys))):
                self.fill_network(self.__Neys[j].Value)
                ans = self.decide()
                print(ans[0])
                if ans[0] != self.__Neys[j].Value:
                    i += 1
                    self.teach(self.__Neys[j].Value)




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
# n = Net(40, 10, 5, (183, 111, 11, 255))
# n.force_teach()
# n.cut_digits(p)
# cls = max(p.getcolors(), key=lambda x: x[0])[0]
# cls /= p.size[0]*p.size[1]
# print(cls)
# for i in n.digits:
#     buff = i[0].getcolors()
#     buff = [x[0] for x in buff if x[1] == n.back]
#     buff[0] /= i[0].size[0]*i[0].size[1]
#     print(buff[0])
#     # i[0].show()
p=[[]]*3
p[0].append(4)
print(p)