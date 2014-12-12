#!/usr/bin/python

import unittest
import sys

import testhelper as t
t.register_maincodefolder()
# Get module under test
import Get_Weather_Files as gwf


class Tests_ParseContentTypeForHTMLText(unittest.TestCase):
    
    def setUp(self):
        # Effectively just an alias to make calls more concise
        self._parsefunc = gwf.ParseContentTypeForHTMLText
    
    def test_texthtmltype_explicitencoding(self):
        istexthtml, encoding = self._parsefunc('text/html;charset=ISO-8859-1')
        self.assertTrue(istexthtml)
        self.assertEqual(encoding, 'ISO-8859-1')

    def test_texthtmltype_usedefaultencoding(self):
        istexthtml, encoding = self._parsefunc('text/html')
        self.assertTrue(istexthtml)
        self.assertEqual(encoding, 'utf-8')
    
    def test_othertype(self):
        istexthtml, encoding = self._parsefunc('text/json')
        self.assertFalse(istexthtml)
        self.assertEqual(encoding, None)


class MockHTTPResponse(object):
    
    def _UTF8String(self, string):
        if sys.version_info.major >= 3:
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


class Tests_GetHTMLTextFromResponse(unittest.TestCase):
    
    def test_htmlresponse_getstext(self):
        inputtext = '<html></html>'
        response = MockHTTPResponse('text/html', inputtext)
        outputtext = gwf.GetHTMLTextFromResponse(response)
        self.assertEqual(inputtext, outputtext)
            
    def test_nonhtmlresponse_raisesexception(self):
        response = MockHTTPResponse('text/xml', '<xml></xml>')
        thrownexception = None # Initial state
        try:
            outputtext = gwf.GetHTMLTextFromResponse(response)
        except Exception as e:
            thrownexception = e
        self.assertEqual(type(thrownexception), type(Exception()))
        self.assertEqual(str(thrownexception),
                         'Response content is not TEXT/HTML.')


if __name__ == '__main__':
    unittest.main()
