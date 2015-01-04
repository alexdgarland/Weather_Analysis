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
 
    def test_size_conversion_bad_exponent_format_gets_none(self):
        file = self._construct_file_with_size('5MG')
        self.assertEqual(None, file.size_bytes)

    def test_size_conversion_bad_number_format_gets_none(self):
        file = self._construct_file_with_size('5.3.3M')
        self.assertEqual(None, file.size_bytes)


class Tests_WeatherDataFile_DateConversions(unittest.TestCase):

    def _construct_file_with_date(self, date):
        f = wdf.WeatherDataFile('test file', '<link>', date, '2.4M')
        return f
    
    def test_valid_datestring_converted(self):
        expecteddate = dt.datetime(2012, 3, 19, 12, 57)
        file = self._construct_file_with_date('19-Mar-2012 12:57')
        self.assertEqual(expecteddate, file.modified_date)

    def test_bad_datestring_gets_none(self):
        file = self._construct_file_with_date('ASDF')
        self.assertEqual(None, file.modified_date)
        

class Tests_WeatherDataFile_ObjectOverrides(unittest.TestCase):
    
    def test_print_weather_data_file(self):
        expected = 'File "test file" available via HTTP at <link>. '
        expected = expected + 'Modified at 01-Jan-2014 12:30:00, size 2.4M.'
        file = wdf.WeatherDataFile('test file', '<link>',
                                   '01-Jan-2014 12:30:00', '2.4M')
        actual = '{0}'.format(file)
        self.assertEqual(expected, actual)


class Tests_WeatherDataFile_UpdateName(unittest.TestCase):
    
    def test_updatename(self):
        file = wdf.WeatherDataFile('test_file.csv', '<link>',
                                   '01-Jan-2014 12:30', '2.4M')
        expectedname = 'test_file_20140101_1230.csv'
        self.assertEqual(expectedname, file.updatename)


if __name__ == '__main__':
    unittest.main()

