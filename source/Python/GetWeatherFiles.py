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
        current_file_state = store.RegisterFile(f, load_id)
        print("File state is recorded as \"{0}\"".format(current_file_state))
        
        if current_file_state == 'registered':
            print('\nDOWNLOADING FILE ', f.filename)
            print('FROM ', f.link)
            print('TO {0} (as {1})\n'.format(targetdirectory, f.downloadname))            
            f.download(targetdirectory)            
            store.LogDownload(f, load_id)
    
    print("Finished!")

