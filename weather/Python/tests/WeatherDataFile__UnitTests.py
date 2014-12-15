#!/usr/bin/python

import unittest
import testhelper as t
t.register_maincodefolder()
# Get module under test
import WeatherDataFile as wdf
import datetime as dt


class Tests_WeatherDataFile_SizeConversions(unittest.TestCase):
    
    def _construct_file_with_size(self, size):
        f = wdf.WeatherDataFile('test file', '<link>', dt.datetime.now(), size)
        return f
    
    def test_size_conversion_from_bytes(self):
        file = self._construct_file_with_size('669')
        self.assertEqual(669, file.size_bytes)

    def test_size_conversion_from_kilobytes(self):
        file = self._construct_file_with_size('501K')
        self.assertEqual(513024, file.size_bytes)
    
    def test_size_conversion_from_megabytes(self):
        file = self._construct_file_with_size('2.4M')
        # Rounding the result of 2.4 * 1024 * 1024 to an integer
        self.assertEqual(2516582, file.size_bytes)

    def test_size_conversion_from_gigabytes(self):
        # Don't expect to ever deal with files this size
        # (and don't want to store >32-bit ints in the DB)
        # but test for handling anyway so code can screen and throw exceptions.
        file = self._construct_file_with_size('5G')
        self.assertEqual(5368709120, file.size_bytes)
        
    def test_size_conversion_bad_exponent_gets_none(self):
        file = self._construct_file_with_size('5Z')
        self.assertEqual(None, file.size_bytes)
 
    def test_size_conversion_bad_format_gets_none(self):
        file = self._construct_file_with_size('5MG')
        self.assertEqual(None, file.size_bytes)
       

if __name__ == '__main__':
    unittest.main()

