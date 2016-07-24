""" Unit test for convert functions """

import unittest

from .. import convert

class TestConvertUnit(unittest.TestCase):
    """ Test unit function """
    def test_unit(self):
        """ Simple test """
        value = convert.unit([10, 0], 0)
        self.assertEqual(10, value)
    def test_unit_not_first_value(self):
        """ Simple test not first value """
        value = convert.unit([10, 11, 12, 13], 2)
        self.assertEqual(12, value)

class TestConvertTenth(unittest.TestCase):
    """ Test tenth function """
    def test_simple(self):
        """ Simple test """
        value = convert.tenth([10, 0], 0)
        self.assertEqual(1.0, value)
    def test_not_first_value(self):
        """ Simple test not first value """
        value = convert.tenth([10, 11, 12, 13], 2)
        self.assertEqual(1.2, value)
    def test_negative_value(self):
        """ Simple test negative value """
        value = convert.tenth([10, 32792, 12, 13], 1)
        self.assertEqual(-2.4, value)
    def test_no_value(self):
        """ Simple test for special no value """
        value = convert.tenth([10, 32792, 0xFFFF, 13], 2)
        self.assertEqual(None, value)

class TestConvertUnitAndTen(unittest.TestCase):
    """ Test unit_and_ten function """
    def test_simple(self):
        """ Simple test """
        value = convert.unit_and_ten([9, 10], 0)
        self.assertEqual(109, value)

class TestConvertWriteUnit(unittest.TestCase):
    """ Test write_unit function """
    def test_simple(self):
        """ Simple test """
        value = convert.write_unit(105)
        self.assertEqual([105], value)
    def test_string(self):
        """ Simple string test """
        value = convert.write_unit("105")
        self.assertEqual([105], value)

class TestConvertWriteTenth(unittest.TestCase):
    """ Test write_tenth function """
    def test_simple(self):
        """ Simple test """
        value = convert.write_tenth(10.5)
        self.assertEqual([105], value)
    def test_string(self):
        """ Simple string test """
        value = convert.write_tenth("10.5")
        self.assertEqual([105], value)
    def test_negative_value(self):
        """ Test with negative value """
        value = convert.write_tenth(-10.5)
        self.assertEqual([0x8069], value)
