#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Data.pixel import Pixel


class Patch(object):

    def __init__(self, start_pixel=Pixel(), end_pixel=Pixel()):
        self.start_pixel = start_pixel
        self.end_pixel = end_pixel

        assert self.isValid()
        return

    def isValid(self):
        if self.start_pixel.x >= self.end_pixel.x:
            return False
        if self.start_pixel.y >= self.end_pixel.y:
            return False
        return True

    @classmethod
    def fromList(cls, xy_xy_list):
        return cls(Pixel.fromList(xy_xy_list[0]),
                   Pixel.fromList(xy_xy_list[1]))

    def getArea(self):
        return (self.end_pixel.x - self.start_pixel.x +
                1) * (self.end_pixel.y - self.start_pixel.y + 1)

    def toList(self):
        return [self.start_pixel.toList(), self.end_pixel.toList()]

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[Patch]")
        print(line_start + "\t start_pixel :")
        self.start_pixel.outputInfo(info_level + 1)
        print(line_start + "\t end_pixel :")
        self.end_pixel.outputInfo(info_level + 1)
        return True
