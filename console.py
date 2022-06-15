# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:54:34 2022

@author: Ale
"""
import sys


def printnew(text):
    if type(text) != str:
        text = str(text)
    sys.stdout.write("\r")
    sys.stdout.write("\r" + text)
    sys.stdout.flush()
