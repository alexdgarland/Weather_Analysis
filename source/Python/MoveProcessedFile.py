#!/usr/bin/python

# Simple cross-platform script to move a given file(name)
# from "downloaded" to "processed" folder

import os
import sys


getdir = os.path.dirname
datadir = os.path.join(getdir(getdir(getdir(__file__))), "data")


def MoveFile(filename):
    src=os.path.join(datadir,"downloaded",filename)
    dst=os.path.join(datadir,"processed",filename)
    print("Archiving data file from {0} to {1}".format(src,dst))
    os.rename(src, dst)


def GetFileNameFromArgs(args):
    if len(args) < 2:
        raise Exception("Filename not supplied")
    else:
        return args[1]


if __name__ == '__main__':
    
    filename = GetFileNameFromArgs(sys.argv)
    MoveFile(filename)
