#!/usr/bin/python

import re # regex

class HTMLResponse(object):
    
    def __init__(self, httpresponse):
        if httpresponse.getheader('Content-Type')[:9] != 'text/html':
            raise ValueError('Response content type is not text/html')
        else:
            self._httpresponse = httpresponse
        
    def _getheader(self, name):        
        return self._httpresponse.getheader(name)
        
    @property
    def encoding(self):
        contenttype = self._getheader('Content-Type')
        result = re.match('[\S]+charset=([\S]+)', contenttype)
        if result is None:
            return 'utf-8'
        else:
            return result.group(1)
            
    @property
    def bodytext(self):
        responsebytes = self._httpresponse.read()
        return responsebytes.decode(self.encoding)

