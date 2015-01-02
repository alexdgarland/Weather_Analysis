#!/usr/bin/python
import sys

class MockHTTPResponse(object):
    
    def _UTF8String(self, string):
        if sys.version_info[0] >= 3:
            return string
        else:
            return(unicode(string, 'utf-8'))    
    
    def __init__(self, contenttype, bodytext):
        self._contenttype = contenttype
        self._utf8_bodytext = self._UTF8String(bodytext)
    def getheader(self, name):
        if name == 'Content-Type':
            return self._contenttype
        else:
            return None
    def read(self):
        return self._utf8_bodytext.encode('utf-8')
        
