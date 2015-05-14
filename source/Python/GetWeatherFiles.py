#!/usr/bin/python


import os.path as op
import sys
import Postgres.FileListStore as pg
from FileList import FileList


def GetDownloadDirectory():
    scriptpath = op.realpath(__file__)
    repository_root = op.dirname(op.dirname(op.dirname(scriptpath)))
    return op.join(repository_root, 'data', 'downloaded')


def GetLoadIDFromArgs(args):
    if len(args) > 1:
        try:
            load_id = int(args[1])
        except ValueError:
            raise ValueError('Command-line argument must be an integer LoadID')
        return load_id
    else:
        return None


if __name__ == '__main__':
    
    # Set up
    targetdirectory = GetDownloadDirectory()    
    store = pg.PostgresFileListStore()
    
    # Get load ID, either from command line or database
    load_id = GetLoadIDFromArgs(sys.argv)
    if load_id is not None:
        if not (store.LoadIsActive(load_id)):
            raise Exception('Load for supplied ID is not active')
    else:
        load_id = store.GetLoadID()
    

    # Loop through list of available files and download
    
    for file in FileList('http://www.geos.ed.ac.uk/~weather/jcmb_ws/').GetFiles():

        print('\n' + str(file))
        current_file_state = store.RegisterFile(file, load_id)
        print("File state is recorded as \"{0}\".".format(current_file_state))
        
        if current_file_state == 'registered':
            print('\nDOWNLOADING FILE ', file.filename)
            print('FROM ', file.link)
            print('TO {0} (as {1})\n'.format(targetdirectory, file.downloadname))            
            file.download(targetdirectory)            
            store.LogDownload(file, load_id)
    
    print("Finished!")

