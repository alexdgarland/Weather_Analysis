#!/usr/bin/python

import os.path as op
import sys

# Get Postgres set-up code
source_root = op.dirname(op.dirname(op.realpath(__file__)))
sys.path.append(op.join(source_root, 'Python'))

from Postgres import SetUp

import datetime as dt


def GetDefaultLogger():
    logpath = op.join(op.dirname(op.realpath(__file__)), 'DBBuild.log')
    def Logger(message, mode='a+'):
        with open(logpath, mode) as f:
            f.write(message)
    return Logger


class PGSQLScriptRunner(object):
    """
    Simple class to pull DDL query from text file
    and run against default DB connection.
    """
    
    def __init__(self, logger=None):
        self._conn = SetUp.GetDefaultConnection()
        self._scriptdir = op.join(op.dirname(op.realpath(__file__)), 'schema')
        self._logger = logger or GetDefaultLogger()

    def _get_querytext(self, ScriptName):
        scriptpath = op.join(self._scriptdir, ScriptName)
        with open(scriptpath, 'r+', encoding='utf-8-sig') as f:
            querytext = f.read()
        return querytext

    def LogStart(self):
        msg = "****** Starting build at {0} *****\n"
        self._logger(msg.format(dt.datetime.now()), mode='w+')

    def RunScript(self, ScriptName):
        query = self._get_querytext(ScriptName)
        self._logger("\n*** Executing script \"{0}\" ***\n".format(ScriptName))
        self._logger(query + "\n")
        with self._conn.cursor() as cur:
            cur.execute(query)
            self._conn.commit()
        self._logger("*** OK ***\n")
        
    def __del__(self):
        self._conn.close()


def GetBuildList():
    """
    Get list of scripts to run in order from simple "BuildList" text file.
    """
    buildlist = op.join(
                        op.dirname(op.realpath(__file__)),
                        'schema',
                        'BuildList.txt'
                        )

    def _isComment(line):
        return line[0] == '#'
        
    with open(buildlist, 'r+') as f:
        for line in f.readlines():
            line = line.replace('\n', '').strip()
            if line != '' and not _isComment(line):
                yield line
        

def BuildDatabase():

    runner = PGSQLScriptRunner()

    runner.LogStart()

    # Run each script against database in order
    for scriptname in GetBuildList():
        print(scriptname)
        runner.RunScript(scriptname)
    

if __name__ == '__main__':
    
    BuildDatabase()
