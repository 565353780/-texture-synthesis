#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Pixel(object):

    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)
        return

    @classmethod
    def fromList(cls, xy_list):
        return cls(xy_list[0], xy_list[1])

    def toList(self):
        return [self.x, self.y]

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[Pixel]")
        print(line_start + "\t position: [" + str(self.x) + ", " +
              str(self.y) + "]")
        return True
