#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../ControlNet-v1-1-nightly')

from texture_synthesis.Module.sd_server import SDServer


def demo():
    sd_server = SDServer()
    sd_server.start()
    return True
