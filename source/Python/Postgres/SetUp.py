#!/usr/bin/python

import configparser as cp
import os
import os.path as osp
import psycopg2 as pg


def GetConfigParser(filename='PostgresConnection.cfg'):
    configpath = osp.join(os.environ['PythonAppConfigFolder'], filename)
    parser = cp.SafeConfigParser()
    parser.read(configpath)
    return parser
    
def GetDefaultConnection(parser=None):
    parser = parser or GetConfigParser()
    return pg.connect(
            host=parser.get("server","host"),
            port=parser.get("server","port"),
            user=parser.get("credentials","user"),
            password=parser.get("credentials","password"),
            database=parser.get("weatheranalysis","database_name")
            )