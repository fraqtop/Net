# -*- coding: utf-8 -*- #
from Net.Neyron import Ney
from PIL import Image, ImageDraw

class Net:
    def __init__(self, newpic, newdelta, newscale, newpixcount):
        self.__Neys = []
        for i in range(10):
            self.__Neys.append(Ney(i))
        if isinstance(newpic, Image.Image):
            self.picsize = (newpic.size[0], newpic.size[1])
            self.picture = newpic
            self.__window = [self.picsize[1], self.picsize[0], 0, 0]
            self.__draw = ImageDraw.Draw(self.picture)
            self.__back = max(newpic.getcolors())[1]
            self.delta = newdelta
            self.scale = newscale
            self.pixcount = newpixcount

    def out_of_range(self, col):
        if sum(self.__back)-self.delta < sum(col) < sum(self.__back)+self.delta:
            return False
        return True

    def cut_digits(self):
        pixmap = self.picture.load()
        for j in range(self.picsize[0]-self.scale):
            for i in range(self.picsize[1]-self.scale):
                if self.out_of_range(pixmap[j, i]) and self.__is_outside(i, j):
                    if self.__resp_area(self.picture.crop((j-self.scale, i-self.scale, j+self.scale, i+self.scale))):
                        self.__window[0] = min((self.__window[0], j-self.scale))
                        self.__window[1] = min((self.__window[1], i-self.scale))
                        self.__window[2] = max((self.__window[2], j+self.scale))
                        self.__window[3] = max((self.__window[3], i+self.scale))
        return self.picture.crop(self.__window)

    def __resp_area(self, rect):
        if isinstance(rect, Image.Image):
            cols = rect.getcolors()
            for i in cols:
                if i[0] > self.pixcount and self.out_of_range(i[1]):
                    # drw = ImageDraw.Draw(rect)
                    # for i in range(rect.width):
                    #     for j in range(rect.height):
                    #         if rect.getpixel((i, j)) == (0, 0, 0):
                    #             drw.point((i, j),(255, 0, 0))
                    # rect.show()
                    return True
        return False

    def __is_outside(self, i, j):
        if self.__window[1] < i < self.__window[3] and self.__window[0] < j < self.__window[2]:
            return False
        return True


p = Image.open('qwe.png')
n = Net(p, 40, 20, 100)
n.cut_digits().show()