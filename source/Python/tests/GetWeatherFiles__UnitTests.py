#!/usr/bin/python

import unittest
import testhelper as t
t.register_maincodefolder()
# Get module under test
import GetWeatherFiles as gwf
import WeatherDataFile as wdf

class Tests_GetFilesFromTable(unittest.TestCase):

    def setUp(self):    
        t = []
        t.append(['', 'Name', 'Last modified', 'Size', 'Description'])
        t.append(['', {'text': 'Parent Directory', 'href': '/~weather/'},
                  '', '-', ''])
        t.append(['', {'text': 'CR10X1.DAT', 'href': 'CR10X1.DAT'},
                  '15-Dec-2014 04:00', '308M', ''])
        t.append(['', {'text': 'JCMB_2006.csv', 'href': 'JCMB_2006.csv'}, 
                  '19-Mar-2012 12:57', '19M', ''])
        self._table = t
        self._csvfile = wdf.WeatherDataFile('JCMB_2006.csv', 'JCMB_2006.csv',
                                            '19-Mar-2012 12:57', '19M')
        self._datfile = wdf.WeatherDataFile('CR10X1.DAT', 'CR10X1.DAT',
                                            '15-Dec-2014 04:00', '308M')

    def _filelists_equal(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for index, file in enumerate(list1):
            if file.__dict__ != list2[index].__dict__:
                return False
        return True

    def test_get_all_files(self):
        expectedlist = [self._datfile, self._csvfile]
        files = gwf.GetFilesFromTable(self._table, url='')
        self.assertTrue(self._filelists_equal(expectedlist, files))

    def test_get_csv_files_only(self):
        expectedlist = [self._csvfile]
        files = gwf.GetFilesFromTable(self._table, url='', fileextension='csv')
        self.assertTrue(self._filelists_equal(expectedlist, files))

        
        
if __name__ == '__main__':
    unittest.main()

