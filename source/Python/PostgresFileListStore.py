#!/usr/bin/python

import configparser as cp
import os
import os.path as osp
import psycopg2


# Static setup methods

def get_configparser(filename='PostgresConnection.cfg'):
    configpath = osp.join(os.environ['PythonAppConfigFolder'], filename)
    parser = cp.SafeConfigParser()
    parser.read(configpath)
    return parser
    
def get_defaultconnection(parser=None):
    parser = parser or get_configparser()
    host = parser.get("server", "host")
    port = parser.get("server", "port")
    user = parser.get("credentials", "user")
    password = parser.get("credentials", "password")
    database = parser.get("weatheranalysis", "database_name")    
    return psycopg2.connect(host=host, port=port,
                            database=database,
                            user=user, password=password)    


class PostgresFileListStore(object):
    """
    Concrete class implementing (for Postgres) required operations as defined
    by abstract base class (around file listing and retrieval via HTTP).
    """        
    def __init__(self, connection=None):
        self._conn = connection or get_defaultconnection()

    def GetNewLoadID(self):
        with self._conn.cursor() as cur:
            cur.execute("SELECT staging.\"AssignAndGetNewLoadID\"();")
            self._conn.commit()
            result = cur.fetchone()[0]
        return result

    def InsertIfNew(self, file, load_id):
        with self._conn.cursor() as cur:
            query="SELECT staging.\"InsertFileRecordIfNew\"(%s,%s, %s, %s);"
            params=(file.filename, file.modified_date, file.updatename, load_id)
            cur.execute(query, params)
            self._conn.commit()
            result = cur.fetchone()[0]
        return result
       
    def LogDownload(self, file):
        with self._conn.cursor() as cur:
            query="SELECT staging.\"LogFileDownloadCompletion\"(%s,%s);"
            params=(file.filename, file.modified_date)
            cur.execute(query, params)
            self._conn.commit()
        
    def __del__(self):
        self._conn.close()

