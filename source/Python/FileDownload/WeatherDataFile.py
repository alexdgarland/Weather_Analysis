#!/usr/bin/python

import re # regex
from math import pow
import datetime as dt
import os.path as op

import sys
if sys.version_info[0] >= 3:
    import urllib.request as ur
else:
    import urllib2 as ur


class default_downloader(object):
    "Wrapper round urlretrieve method to make unit testing easier."
    def retrieve(self, url, filename):
        ur.urlretrieve(url, filename)


class WeatherDataFile(object):
    
    def __init__(self, filename, link, modified_date_string, size_string):
        self.filename = filename
        self.link = link
        self._modified_date_string = modified_date_string
        self._size_string = size_string

    @property
    def size_bytes(self):
        regexoutput = re.match('([0-9.]+)([\S]*)', self._size_string)
        if regexoutput is None:
            return None
        exponentpart = regexoutput.group(2).strip()
        try:
            exponent = { '' : 0, 'K' : 1, 'M' : 2, 'G' : 3 }[exponentpart]
        except KeyError:
            return None
        try:
            numericpart = float(regexoutput.group(1))
        except ValueError:
            return None
        return int(numericpart * pow(1024, exponent))

    @property
    def modified_date(self):
        try:
            fmt = '%d-%b-%Y %H:%M'
            return dt.datetime.strptime(self._modified_date_string, fmt)
        except ValueError:
            return None
    
    @property
    def downloadname(self):
        regexoutput = re.match('([A-Za-z0-9_\s]+)(.[A-Za-z]+)', self.filename)
        basename, extension = regexoutput.group(1), regexoutput.group(2)
        formatted_date = self.modified_date.strftime('%Y%m%d_%H%M')
        return basename + '_' + formatted_date + extension
        
    def download(self, targetdirectory, downloader=default_downloader()):
        targetfile = op.join(targetdirectory, self.downloadname)
        downloader.retrieve(self.link, targetfile)  
        
    def __str__(self):
        fmt = 'File "{0}" available via HTTP at {1}. '
        fmt = fmt + 'Modified at {2}, size {3}.'
        return fmt.format(self.filename, self.link, self._modified_date_string,
                          self._size_string)

