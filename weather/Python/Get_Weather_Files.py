#!/usr/bin/python

import HTMLResponse as hr

import sys
if sys.version_info[0] >= 3:
    import urllib.request as ur
else:
    import urllib2 as ur



if __name__ == '__main__':

    httpresponse = ur.urlopen('http://www.geos.ed.ac.uk/~weather/jcmb_ws/')
    
    htmlresponse = hr.HTMLResponse(httpresponse)

    print(htmlresponse.bodytext)
    
