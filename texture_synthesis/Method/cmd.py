#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess


def runCMD(cmd):
    ex = subprocess.Popen(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding="utf-8")
    ex.communicate()
    state = ex.wait()
    return state == 0
