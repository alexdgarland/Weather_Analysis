import sys
import os.path as op

def register_maincodefolder():
    # Get folder this script is in
    testscriptpath = op.realpath(__file__)
    testscriptfolder = op.split(testscriptpath)[0]
    # Step up one from the folder the file is in
    maincodefolder = op.split(testscriptfolder)[0]
    # Add that folder (containing code under test) to import path
    sys.path.append(maincodefolder)
    