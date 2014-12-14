#!/usr/bin/python

import unittest
import testhelper as t
t.register_maincodefolder()
# Get module under test
import HTMLTableParser as htp


def get_expectedtable():
    table = []
    table.append(['', 'Name', 'Last modified', 'Size', 'Description'])
    table.append(['', {'href':'/~weather/','text':'Parent Directory'},
                      '' , '-' ,''])
    table.append(['', {'href':'CR10X1.DAT','text':'CR10X1.DAT'},
                      '12-Dec-2014 22:00','307M', ''])
    table.append(['', {'href':'JCMB_2006.csv','text':'JCMB_2006.csv'},
                      '19-Mar-2012 12:57', '19M', ''])
    table.append(['', {'href':'JCMB_2006_Aug.csv','text':'JCMB_2006_Aug.csv'},
                      '19-Mar-2012 12:58', '2.5M', ''])
    table.append(['', {'href':'JCMB_2014_Jun.csv','text':'JCMB_2014_Jun.csv'},
                      '07-Nov-2014 10:52', '2.5M', ''])
    return table


class Tests_HTMLTableParser(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_table_as_expected(self):
        # ARRANGE - Set up nested list we want from parsing the HTML table
        expectedtable = get_expectedtable()        
        # ACT - parse some HTML
        examplehtml = t.get_testdata_text('WeatherFile_Index_Example.html')
        parser = htp.HTMLTableParser()
        actualtable = parser.GetTable(examplehtml)        
        # ASSERT
        self.assertEqual(expectedtable, actualtable)


if __name__ == '__main__':
    unittest.main()
