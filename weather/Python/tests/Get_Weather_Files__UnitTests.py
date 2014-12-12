#!/usr/bin/python

import unittest

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



if __name__ == '__main__':
    unittest.main()