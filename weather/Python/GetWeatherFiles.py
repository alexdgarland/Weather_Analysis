#!/usr/bin/python

from HTMLResponse import HTMLResponse
from HTMLTableParser import HTMLTableParser
from WeatherDataFile import WeatherDataFile
import os.path as op

import sys
if sys.version_info[0] >= 3:
    import urllib.request as ur
else:
    import urllib2 as ur


indexurl = 'http://www.geos.ed.ac.uk/~weather/jcmb_ws/'


def GetFilesFromTable(table, url=indexurl, fileextension=None):
    """
    Take a table (nested list, parsed from HTML)
    and output a list of file objects for each relevant row.
    """
    def _isfilerow(row):
        return (row[1] != 'Name' and row[3] != '-')

    def _matchesextension(filename):
        if fileextension is None:
            return True
        else:
            return (filename.endswith(fileextension))

    files = []
    for row in table:    
        if _isfilerow(row):
            filename = row[1]['text']
            if _matchesextension(filename):
                link = op.join(url, row[1]['href'])
                date = row[2]
                size = row[3]
                files.append(WeatherDataFile(filename, link, date, size))   
    return files



if __name__ == '__main__':

    httpresponse = ur.urlopen(indexurl)
    
    htmlresponse = HTMLResponse(httpresponse)
    
    table = HTMLTableParser().GetTable(htmlresponse.bodytext)

    files = GetFilesFromTable(table, fileextension='csv')


    # List and download files 
    
    targetdirectory = op.join(op.split(op.split(op.realpath(__file__))[0])[0],
                                       'data', 'downloaded')

    for f in files:
        print('\n' + str(f))
        print('\nDOWNLOADING FILE "{0}" \nFROM {1} \nTO {2}\n\n'.format(
            f.filename, f.link, targetdirectory))
        f.download(targetdirectory)
    
    print("Finished!")
