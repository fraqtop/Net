# -*- coding: utf-8 -*- #
from Net.Neyron import Ney
from PIL import Image, ImageDraw

class Net:
    def __init__(self, newpic, newdelta):
        self.__Neys = []
        for i in range(10):
            self.__Neys.append(Ney(i))
        if isinstance(newpic, Image.Image):
            self.picsize = (newpic.size[0], newpic.size[1])
            self.picture = newpic
            self.__window = [0, 0, 0, 0]
            self.__map = self.picture.load()
            self.__draw = ImageDraw.Draw(self.picture)
            self.__back = max(newpic.getcolors())[1]
            self.delta = newdelta

    def cut_digits(self):
        pixmap = self.picture.load()
        for j in range(self.picsize[0]):
            for i in range(self.picsize[1]):
                if pixmap[j, i] != self.__back:
                    self.__window = [i-1, j-1, i+1, j+1]
                    self.__draw.point((i, j), (255, 0, 0))
                    self.__resp_area(i+1, j)
                    self.__resp_area(i, j+1)
                    self.__resp_area(i-1, j+1)
                    self.__resp_area(i+1, j+1)
                    self.__resp_area(i-1, j)
                    return self.picture.crop(self.__window)

    def __resp_area(self, x, y):
        if self.__map[y, x] != self.__back and self.__is_outside(x, y):
            if x <= self.__window[0]:
                self.__window[0] = x-1
            if x >= self.__window[2]:
                self.__window[2] = x+1
            if y >= self.__window[3]:
                self.__window[3] = y+1
            if y <= self.__window[1]:
                self.__window[1] = y-1
            self.__resp_area(x+1, y)
            self.__resp_area(x, y+1)
            self.__resp_area(x-1, y+1)
            self.__resp_area(x+1, y+1)
            self.__resp_area(x-1, y)

    def __resp_area2(self, rect):
        if isinstance(rect, Image.Image):
            cols = rect.getcolors()
            for i in cols:
                if sum(i[1]) < sum(self.__back)-self.delta or sum(i[1]) > sum(self.__back)+self.delta:
                    return True

    def __is_outside(self, i, j):
        if self.__window[0] < i < self.__window[2] and self.__window[1] < j < self.__window[3]:
            return False
        return True


p = Image.open('qwe.png')
n = Net(p, 40)