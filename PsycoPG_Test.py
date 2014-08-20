# -*- coding: utf-8 -*-

import psycopg2 as pg

def runquery():

    conn = pg.connect(database="AG_Test", user="postgres", password="dummypassword")
    cur = conn.cursor()
    cur.execute('SELECT "RowID", "NumberValue", "TextDescription" FROM "TestTable"')
    
    for c in cur:
        print("LINE: {0}, COMMAND: \"{1}\"".format(c[1], c[2]))


if __name__ == '__main__':
    runquery()