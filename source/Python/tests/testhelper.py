import sys
import os.path as op


def get_testfolder():
    # Get folder this script is in    
    testscriptpath = op.realpath(__file__)
    testscriptfolder = op.split(testscriptpath)[0]
    return testscriptfolder


def register_maincodefolder():
    # Step up one from the folder the file is in
    maincodefolder = op.split(get_testfolder())[0]
    # Add that folder (containing code under test) to import path
    sys.path.append(maincodefolder)


def get_testdata_text(filename, relativepath='testdata'):
    fullfilepath = op.join(get_testfolder(), relativepath, filename)
    with open(fullfilepath, 'r+') as f:
        text = f.read()
    return text
    