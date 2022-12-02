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

    def move(self, move_list):
        self.start_pixel.move(move_list)
        self.end_pixel.move(move_list)
        return True

    def scale(self,
              scale_list,
              start_pixel_list=[-float('inf'), -float('inf')],
              end_pixel_list=[float('inf'), float('inf')]):
        center = self.getCenter()
        half_x_diff = (self.end_pixel.x - self.start_pixel.x) / 2.0
        half_y_diff = (self.end_pixel.y - self.start_pixel.y) / 2.0
        scaled_half_x_diff = int(half_x_diff * scale_list[0])
        scaled_half_y_diff = int(half_y_diff * scale_list[1])

        new_start_x = max(center[0] - scaled_half_x_diff, start_pixel_list[0])
        new_start_y = max(center[1] - scaled_half_y_diff, start_pixel_list[1])
        new_end_x = min(center[0] + scaled_half_x_diff, end_pixel_list[0])
        new_end_y = min(center[1] + scaled_half_y_diff, end_pixel_list[1])
        self.start_pixel.set(new_start_x, new_start_y)
        self.end_pixel.set(new_end_x, new_end_y)
        return True

    def getArea(self):
        return (self.end_pixel.x - self.start_pixel.x +
                1) * (self.end_pixel.y - self.start_pixel.y + 1)

    def getCenter(self):
        x_mean = int((self.start_pixel.x + self.end_pixel.x) / 2)
        y_mean = int((self.start_pixel.y + self.end_pixel.y) / 2)
        return [x_mean, y_mean]

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
