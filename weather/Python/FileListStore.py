#!/usr/bin/python

import configparser as cp
import os
import os.path as osp
import psycopg2
from abc import ABCMeta, abstractmethod


# Static setup methods

def get_configparser(filename='PostgresConnection_Weather.cfg'):
    parser = cp.SafeConfigParser()
    parser.read(osp.join(os.environ['PythonAppConfigFolder'], filename))
    return parser
    
def get_defaultconnection(parser=get_configparser()):
    user = parser.get("credentials", "user")
    password = parser.get("credentials", "password")
    database = parser.get("weatheranalysis", "database_name")    
    return psycopg2.connect(database=database, user=user, password=password)    



class AbstractFileListStore(object):
    """
    Abstract base class defining required datastore operations
    (around file listing and retrieval via HTTP).
    """
    
    # Python-2-style abstract class.
    # If done this way, class can technically be instantiated
    # if run in Python 3 interpreter
    # but alternative (Py3 syntax) won't work in Py2 at all.
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def InsertIfNew(self, file):
        # Needs to return a boolean (true = file is new, needs downloading)     
        pass
    
    @abstractmethod
    def LogDownload(self, file):
        pass


class PostgresFileListStore(AbstractFileListStore):
    """
    Concrete class implementing (for Postgres) required operations as defined
    by abstract base class (around file listing and retrieval via HTTP).
    """        
    def __init__(self, connection=None):
        self._connection = connection or get_defaultconnection()

#    def InsertIfNew(self, file):
#        
#    def LogDownload(self, file):
        
