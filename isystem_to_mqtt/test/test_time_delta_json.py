""" Unit test for custom json encoder """

import unittest
import datetime

from .. import time_delta_json


class TestCustomDateJSONEncoder(unittest.TestCase):
    """ Test DateJSONEnocder """

    def test_timedelta(self):
        """ Test a simple time interval """
        encoder = time_delta_json.CustomDateJSONEncoder()

        result = encoder.encode(datetime.timedelta(hours=11, minutes=35, seconds=12))
        self.assertEqual("\"11:35:12\"", result)

    def test_timedelta_2(self):
        """ Test a simple time interval """
        encoder = time_delta_json.CustomDateJSONEncoder()

        result = encoder.encode(datetime.timedelta(hours=0, minutes=3, seconds=12))
        self.assertEqual("\"00:03:12\"", result)

    def test_timedelta_3(self):
        """ Test a simple time interval """
        encoder = time_delta_json.CustomDateJSONEncoder()

        result = encoder.encode(datetime.timedelta(hours=24, minutes=0, seconds=0))
        self.assertEqual("\"24:00:00\"", result)
