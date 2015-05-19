#!/usr/bin/python


import unittest

import MockHTTPResponse as mhr

import testhelper as t
t.register_maincodefolder()
# Get module under test
import FileDownload.HTMLResponse as hr


class Tests_HTMLResponse(unittest.TestCase):
        
    def test_htmlresponse_constructs_okay(self):
        httpresponse = mhr.MockHTTPResponse('text/html', '<html></html>')
        htmlresponse = hr.HTMLResponse(httpresponse)
        self.assertEqual(hr.HTMLResponse, type(htmlresponse))
        
    def test_nonhtmlresponse_raises_valueerror(self):
        httpresponse = mhr.MockHTTPResponse('text/xml', '<xml></xml>')
        thrownexception = None
        expectedmsg = 'Response content type is not text/html'
        try:
            hr.HTMLResponse(httpresponse)
        except Exception as e:
            thrownexception = e
        self.assertEqual(ValueError, type(thrownexception))
        self.assertEqual(expectedmsg, str(thrownexception))
            
    def test_response_explicitencoding_returnsencoding(self):
        httpresponse = mhr.MockHTTPResponse(
                        'text/html;charset=ISO-8859-1', '<html></html>')
        encoding = hr.HTMLResponse(httpresponse).encoding
        self.assertEqual('ISO-8859-1', encoding)
                        
    def test_response_noencoding_returnsdefaultencoding(self):
        httpresponse = mhr.MockHTTPResponse('text/html', '<html></html>')
        encoding = hr.HTMLResponse(httpresponse).encoding
        self.assertEqual('utf-8', encoding)

    def test_utf8response_getsbodytext(self):
        # NB the mock HTTP response class is only set up to return UTF8
        # so if we did want to test other encodings (probably not needed)
        # would have to extend it.
        inputtext = '<html></html>'
        httpresponse = mhr.MockHTTPResponse('text/html', inputtext)
        outputtext = hr.HTMLResponse(httpresponse).bodytext
        self.assertEqual(inputtext, outputtext)


if __name__ == '__main__':
    unittest.main()

