#!/usr/bin/python

import os.path as op
import os
import subprocess as sp

testfolderpath = op.split(op.realpath(__file__))[0]
filenamesuffix = '__UnitTests.py'

for filename in os.listdir(testfolderpath):
    if filename.endswith(filenamesuffix):
        fullpath = op.join(testfolderpath, filename)
        sp.call("python " + fullpath, shell=True)

