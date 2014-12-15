#!/usr/bin/python

import re # regex
from math import pow

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
        pass

