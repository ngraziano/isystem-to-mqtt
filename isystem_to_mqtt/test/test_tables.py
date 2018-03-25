""" Unit test for tables functions """

import unittest

from .. import tables
from .. import convert


def not_to_be_trantlate(value):
    return value

def no_translation_english(value):
    return value

def translation_english(value):
    return value

def translation_french(value):
    return value


class TestGetConvertionTranslation(unittest.TestCase):
    """ Test the function remplace for translation """
    def test_not_to_be_translate(self):
        """ Test function wich will never be translated """
        result = tables.get_convertion_translation('fr', not_to_be_trantlate)
        self.assertEqual(result, not_to_be_trantlate)

    def test_no_translation(self):
        """ Test function with not translation yet """        
        result = tables.get_convertion_translation('fr', no_translation_english)
        self.assertEqual(result,no_translation_english)

    def test_translation(self):
        """ Test function with translation to french """        
        result = tables.get_convertion_translation('fr', translation_english)
        self.assertEqual(result, translation_french)

    def test_translation_same_lang(self):
        """ Test function with translation keep english """        
        result = tables.get_convertion_translation('en', translation_english)
        self.assertEqual(result,translation_english)



class TestGetTablesTranslated(unittest.TestCase):
    """ Test get table converted function """

    def test_french(self):
        """ Test get french version """
        (readtable, _, _) = tables.get_tables_translated('modulens-o', 'fr')
        decrease_mode_def = readtable.get(10)

        self.assertEqual(decrease_mode_def.convertion, convert.decrease_french)
        mode_def = readtable.get(17)
        self.assertEqual(mode_def.definition_list[0][1],convert.derog_bit_french)
        self.assertEqual(mode_def.definition_list[2][1],convert.derog_bit_simple_french)

    def test_english(self):
        """ Test get english version """
        (readtable, _, _) = tables.get_tables_translated('modulens-o', 'en')
        decrease_mode_def = readtable.get(10)

        self.assertEqual(decrease_mode_def.convertion, convert.decrease_english)
        mode_def = readtable.get(17)
        self.assertEqual(mode_def.definition_list[0][1],convert.derog_bit_english)
        self.assertEqual(mode_def.definition_list[2][1],convert.derog_bit_simple_english)

    