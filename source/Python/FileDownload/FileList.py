#!/usr/bin/python


import os.path as op
import sys
if sys.version_info[0] >= 3:
    import urllib.request as ur
else:
    import urllib2 as ur
import re
from .HTMLResponse import HTMLResponse
from .WeatherDataFile import WeatherDataFile
from .HTMLParsing import HTMLTableParser


defaultfilepattern = 'JCMB_[0-9]{4}_[A-Z][a-z]{2}.csv'


class FileList(object):
    
    
    def __init__(self, url=None):
        self.SetFromURL(url)
        
        
    def SetFromURL(self, url):
        self._url = url
        if url is not None:
            httpresponse = ur.urlopen(url)
            htmlresponse = HTMLResponse(httpresponse)
            parser = HTMLTableParser()
            self._htmlfiletable = parser.GetTable(htmlresponse.bodytext)

        
    def GetFiles(self, filepattern=None):
        
        filepattern = filepattern or defaultfilepattern    
        
        def _isfilerow(row):
            return (row[1] != 'Name' and row[3] != '-')
    
        def _matchespattern(filename):
            return (re.match(filepattern, filename) != None)
    
        files = []
        for row in self._htmlfiletable:    
            if _isfilerow(row):
                filename = row[1]['text']
                if _matchespattern(filename):
                    link = op.join(self._url, row[1]['href'])
                    date = row[2]
                    size = row[3]
                    files.append(WeatherDataFile(filename, link, date, size))   
        return files

