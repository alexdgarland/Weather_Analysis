#!/usr/bin/python

from . import SetUp

class PostgresFileListStore(object):
    """
    Postgres imlementation of required database operations
    (around file listing and retrieval via HTTP).
    """
    
    def __init__(self, connection=None):
        self._conn = connection or SetUp.GetDefaultConnection()

    def GetLoadID(self):
        with self._conn.cursor() as cur:
            cur.execute("SELECT staging.\"GetLoadID\"();")
            self._conn.commit()
            result = cur.fetchone()[0]
        return result

    def RegisterFile(self, file, load_id):
        with self._conn.cursor() as cur:
            query="SELECT out_current_state FROM staging.\"RegisterFile\"(%s,%s,%s);"
            params=(file.filename, file.modified_date, load_id)
            cur.execute(query, params)
            self._conn.commit()
            result = cur.fetchone()[0]
        return result
       
    def LogDownload(self, file, load_id):
        with self._conn.cursor() as cur:
            query="SELECT staging.\"LogFileDownloadCompletion\"(%s,%s,%s,%s);"
            params=(file.filename, file.modified_date, file.downloadname, load_id)
            cur.execute(query, params)
            self._conn.commit()
            
    def LoadIsActive(self, load_id):
        with self._conn.cursor() as cur:
            query="SELECT staging.\"LoadIsActive\"(%s);"
            params = (load_id,)            
            cur.execute(query, params)
            self._conn.commit()
            result = cur.fetchone()[0]
        return result
        
    def __del__(self):
        self._conn.close()

