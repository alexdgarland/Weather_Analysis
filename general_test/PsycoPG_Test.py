# -*- coding: utf-8 -*-

import psycopg2 as pg
import configparser as cp
import os.path as osp
import os

def getconfigparser():
    pyconfigdir = os.environ['PythonAppConfigFolder']
    cfglocation = osp.join(pyconfigdir, "PostgresCredentials.cfg")
    parser = cp.SafeConfigParser()
    parser.read(cfglocation)
    return parser

def getcredentials(parser, section="ADMIN"):
    user = parser.get(section, "user")
    password = parser.get(section, "password")
    return (user, password)

def runquery(querytext):
    parser = getconfigparser()    
    user, password = getcredentials(parser)
    conn = pg.connect(database="AG_Test", user=user, password=password)
    cur = conn.cursor()
    cur.execute(querytext)
    return [c for c in cur]     # return results as a list


def main():    

    sql = 'SELECT "RowID", "NumberValue", "TextDescription" FROM "TestTable"'

    for r in runquery(sql):
        print("LINE: {0}, COMMAND: \"{1}\"".format(r[1], r[2]))


if __name__ == '__main__':    
    main()
