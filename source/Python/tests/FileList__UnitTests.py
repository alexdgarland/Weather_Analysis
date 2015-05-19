#!/usr/bin/python


import unittest
import testhelper as t
t.register_maincodefolder()
# Get module under test
import FileList as f
import WeatherDataFile as wdf
import os.path as op


class Tests_GetFilesFromTable(unittest.TestCase):


    def setUp(self):
        
        t = []
        t.append(['', 'Name', 'Last modified', 'Size', 'Description'])
        t.append(['', {'text': 'Parent Directory', 'href': '/~weather/'},
                  '', '-', ''])
        t.append(['', {'text': 'CR10X1.DAT', 'href': 'CR10X1.DAT'},
                  '15-Dec-2014 04:00', '308M', ''])
        t.append(['', {'text': 'JCMB_2006_Mar.csv', 'href': 'JCMB_2006_Mar.csv'}, 
                  '19-Mar-2012 12:57', '19M', ''])

        self._filelist = f.FileList()
        self._filelist._htmlfiletable = t        
        self._filelist._url = "<URL>"        
        
        self._csvfile = wdf.WeatherDataFile('JCMB_2006_Mar.csv', op.join('<URL>', 'JCMB_2006_Mar.csv'),
                                            '19-Mar-2012 12:57', '19M')
        self._datfile = wdf.WeatherDataFile('CR10X1.DAT', op.join('<URL>', 'CR10X1.DAT'),
                                            '15-Dec-2014 04:00', '308M')


    def _lists_of_files_equal(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for index, file in enumerate(list1):
            if file.__dict__ != list2[index].__dict__:
                return False
        return True


    def test_get_default_format(self):
        expectedlist = [self._csvfile]
        files = self._filelist.GetFiles()
        self.assertTrue(self._lists_of_files_equal(expectedlist, files))


    def test_get_dat_format(self):
        expectedlist = [self._datfile]
        files = self._filelist.GetFiles('CR[A-Za-z0-9]+\.DAT')
        self.assertTrue(self._lists_of_files_equal(expectedlist, files))
        
        
if __name__ == '__main__':
    unittest.main()

