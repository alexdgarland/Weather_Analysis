#!/usr/bin/python

from . import SetUp

class PostgresFileListStore(object):
    """
    Postgres imlementation of required database operations
    (around file listing and retrieval via HTTP).
    """
    
    def __init__(self, connection=None):
        self._conn = connection or SetUp.GetDefaultConnection()

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

