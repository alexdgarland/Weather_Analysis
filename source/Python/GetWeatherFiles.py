#!/usr/bin/python


import os.path as op
import Postgres.FileListStore as pg
from FileList import FileList


def GetDownloadDirectory():
    scriptpath = op.realpath(__file__)
    repository_root = op.dirname(op.dirname(op.dirname(scriptpath)))
    return op.join(repository_root, 'data', 'downloaded')


if __name__ == '__main__':
    
    # List, download and log files 
    targetdirectory = GetDownloadDirectory()
    
    store = pg.PostgresFileListStore()
    load_id = store.GetNewLoadID()
    
    for f in FileList('http://www.geos.ed.ac.uk/~weather/jcmb_ws/').GetFiles():

        print('\n' + str(f))
        
        if store.InsertIfNew(f, load_id):
            print('\nDOWNLOADING FILE ', f.filename)
            print('FROM ', f.link)
            print('TO {0} (as {1})\n'.format(targetdirectory, f.updatename))            
            f.download(targetdirectory)            
            store.LogDownload(f)
        else:
            print("File \"{0}\" already logged as downloaded.".format(f.filename))
    
    print("Finished!")

