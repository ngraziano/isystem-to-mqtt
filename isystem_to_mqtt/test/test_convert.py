""" Unit test for convert functions """

import unittest
import datetime

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

class TestConvertAnticipation(unittest.TestCase):
    """ Test powe function """

    def test_simple(self):
        """ Simple test """
        value = convert.anticipation([1, 2, 3], 0)
        self.assertEqual(0.1, value)

    def test_none(self):
        """ Test Maximum value """
        value = convert.anticipation([101, 999, 999], 0)
        self.assertEqual(None, value)


class TestConvertPower(unittest.TestCase):
    """ Test powe function """

    def test_simple(self):
        """ Simple test """
        value = convert.power([1, 2, 3], 0)
        self.assertEqual(1002003, value)

    def test_max_value(self):
        """ Test Maximum value """
        value = convert.power([999, 999, 999], 0)
        self.assertEqual(999999999, value)

    def test_no_value(self):
        """ Test Maximum value """
        value = convert.power([65535, 65535, 65535], 0)
        self.assertEqual(None, value)


class TestConvertDerogBitSimple(unittest.TestCase):
    """ Test write_derog_bit_simple function """

    def test_simple(self):
        """ Simple test """
        self.assertEqual("Automatique", convert.derog_bit_simple_french([8], 0))
        self.assertEqual("Jour", convert.derog_bit_simple_french([36], 0))
        self.assertEqual("Jour", convert.derog_bit_simple_french([4], 0))
        self.assertEqual("Nuit", convert.derog_bit_simple_french([34], 0))
        self.assertEqual("Nuit", convert.derog_bit_simple_french([2], 0))
        self.assertEqual("Vacances", convert.derog_bit_simple_french([33], 0))
        self.assertEqual("Vacances", convert.derog_bit_simple_french([1], 0))


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

class TestConvertDaySchedule(unittest.TestCase):
    """ Test day_schedule function """

    def test_empty(self):
        """ empty schedule """
        value = convert.day_schedule([0, 0, 0], 0)
        self.assertEqual([], value)

    def test_full(self):
        """ full schedule always on """
        value = convert.day_schedule([0xFFFF, 0xFFFF, 0xFFFF], 0)
        self.assertEqual([(datetime.timedelta(), datetime.timedelta(days=1))], value)

    def test_onebit_start_end(self):
        """ first half of hours and last half of hours """
        value = convert.day_schedule([0x8000, 0x0000, 0x0001], 0)
        self.assertEqual(
            [
                (datetime.timedelta(), datetime.timedelta(minutes=30)),
                (datetime.timedelta(hours=23, minutes=30), datetime.timedelta(days=1)),
            ], value)

    def test_doc(self):
        """ exemple from documentation """
        value = convert.day_schedule([0x0003, 0xFFFF, 0xFF00], 0)
        self.assertEqual([(datetime.timedelta(hours=7), datetime.timedelta(hours=20))], value)


    def test_half(self):
        """ morning """
        value = convert.day_schedule([0xFFFF, 0xFF00, 0x0000], 0)
        self.assertEqual([(datetime.timedelta(), datetime.timedelta(hours=12))], value)

class TestConvertJsonWeekSchedule(unittest.TestCase):
    """ Test json_week_schedule function """

    def test_empty_week(self):
        """ empty week : always off """
        schedule = [0] * 21

        value = convert.json_week_schedule(schedule, 0)

        self.assertEqual("{\"0\": [], \"1\": [], \"2\": [], \"3\": [], \"4\": [], \"5\": [], \"6\": []}"
                         , value)

    def test_full_week(self):
        """ full week : always on """
        schedule = [0xFFFF] * 21

        value = convert.json_week_schedule(schedule, 0)

        self.assertEqual("{\"0\": [[\"00:00:00\", \"24:00:00\"]], \"1\": [[\"00:00:00\", \"24:00:00\"]], \"2\": [[\"00:00:00\", \"24:00:00\"]], \"3\": [[\"00:00:00\", \"24:00:00\"]], \"4\": [[\"00:00:00\", \"24:00:00\"]], \"5\": [[\"00:00:00\", \"24:00:00\"]], \"6\": [[\"00:00:00\", \"24:00:00\"]]}"
                         , value)

class TestConvertHoursMinutesSecondes(unittest.TestCase):
    """ Test hours_minutes_secondes function """
    def test_simple(self):
        """ simple hours """
        raw = [10, 11, 12]

        value = convert.hours_minutes_secondes(raw, 0)

        self.assertEqual("10:11:12", value)

    def test_simple2(self):
        """ simple hours """
        raw = [1, 2, 3]

        value = convert.hours_minutes_secondes(raw, 0)

        self.assertEqual("01:02:03", value)

class TestConvertDecrese(unittest.TestCase):
    """ Test Decrease function """
    def test_stop_french(self):
        """ test stop """
        raw = [0]

        value = convert.decrease_french(raw, 0)

        self.assertEqual("stop", value)

    def test_decrease_french(self):
        """ test decrease """
        raw = [1]

        value = convert.decrease_french(raw, 0)

        self.assertEqual("abaissement", value)

class TestConvertOffOn(unittest.TestCase):
    """ Test off_on function """
    def test_off(self):
        """ test off """
        raw = [0]

        value = convert.off_on(raw, 0)

        self.assertEqual("off", value)

    def test_on(self):
        """ test on """
        raw = [1]

        value = convert.off_on(raw, 0)

        self.assertEqual("on", value)


class TestConvertOutputState(unittest.TestCase):
    """ Test output_state function """
    def test_all_on(self):
        """ test all on """
        raw = [0xffff, 0xffff]

        value = convert.output_state(raw, 0)
        # TODO check result
        # self.assertEqual("off", value)


class TestConvertText14(unittest.TestCase):
    """ Test Text14 function """
    def test_all_on(self):
        """ test my data """
        raw = [8260,
               18757,
               19777,
               21577,
               17198,
               13344,
               8224,
               8225,
              ]

        value = convert.texte14(raw, 0)
        self.assertEqual(" DIEMATIC.4   ", value)


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

class TestConvertWriteDerogBitSimple(unittest.TestCase):
    """ Test write_derog_bit_simple function """

    def test_simple(self):
        """ Simple test """
        self.assertEqual([8], convert.write_derog_bit_simple("Automatique"))
        self.assertEqual([36], convert.write_derog_bit_simple("Jour"))
        self.assertEqual([34], convert.write_derog_bit_simple("Nuit"))
        self.assertEqual([33], convert.write_derog_bit_simple("Vacances"))

    def test_invalid(self):
        """ invalid value test """
        self.assertIsNone(convert.write_derog_bit_simple("INVALID VALUE"))
