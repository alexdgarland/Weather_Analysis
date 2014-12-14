#!/usr/bin/python

import os.path as op
import subprocess

testfolderpath = op.split(op.realpath(__file__))[0]
command = "cd {0} & python -m unittest discover -p *__UnitTests.py".format(testfolderpath)
subprocess.call(command, shell=True)
