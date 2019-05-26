""" Definition of Modbus adress and convertions to apply """

import sys

from .tag_definition import TagDefinition, WriteTagDefinition, MultipleTagDefinition
from . import convert


def get_tables(model):
    """ Return the address definition depending of model. """
    if model == "modulens-o":
        return (READ_TABLE_MODULENS_OG, WRITE_TABLE_MODULENS_O, ZONE_TABLE_MODULENS_O)
    if model == "modulens-g":
        return (READ_TABLE_MODULENS_OG, WRITE_TABLE_MODULENS_G, ZONE_TABLE_MODULENS_G)
    return (None, None, None)

lang_convertion = {
    'en': '_english',
    'fr': '_french',
}


def get_convertion_translation(lang, convertion):
    """ Select translated function """

    funct_name = convertion.__name__
    if not funct_name.endswith('_english'):
        return convertion

    funct_name = funct_name.replace('_english', lang_convertion.get(lang))
    module = sys.modules[convertion.__module__]
    if hasattr(module, funct_name):
        return getattr(module, funct_name)
    return convertion


def get_definition_translation(lang, value):
    if isinstance(value, TagDefinition):
        return TagDefinition(value.tag_name,
                             get_convertion_translation(
                                 lang, value.convertion),
                             value.needed_value)
    if isinstance(value, MultipleTagDefinition):
        definition_list = [(tagname, get_convertion_translation(lang, convertion))
                           for tagname, convertion in value.definition_list]
        return MultipleTagDefinition(definition_list, value.needed_value)
    return value


def get_tables_translated(model, lang):
    """ Return the address definition depending of model and language."""
    (readtable, writetable, zones) = get_tables(model)

    readtabletranslate = {k: get_definition_translation(lang, v)
                          for k, v in readtable.items()}

    return (readtabletranslate, writetable, zones)

# Table that define the read value
# First value modbus adress
# Second value number of word
ZONE_TABLE_MODULENS_O = [(231, 20),
                         (507, 4),
                         (471, 10),
                         (600, 21),
                         (637, 24),
                         (721, 4),
                         (788, 9), ]

READ_TABLE_MODULENS_OG = {
    3: TagDefinition("boiler/version", convert.unit),
    4: TagDefinition("boiler/time", convert.hours_minutes, 2),
    6: TagDefinition("boiler/dayofweek", convert.unit),
    7: TagDefinition("outside/temperature", convert.tenth),
    8: TagDefinition("boiler/summer-setpoint", convert.tenth),
    9: TagDefinition("outside/antifreeze", convert.tenth),
    10: TagDefinition("boiler/decrease-mode", convert.decrease_english),
    11: TagDefinition("boiler/pump-postrun", convert.unit),
    # FIXME inverse sur ma chaudiere
    12: TagDefinition("boiler/auto-adaptative", convert.off_on),
    14: TagDefinition("zone-a/day-target-temperature", convert.tenth),
    15: TagDefinition("zone-a/night-target-temperature", convert.tenth),
    16: TagDefinition("zone-a/antifreeze-target-temperature", convert.tenth),
    17: MultipleTagDefinition([("zone-a/mode", convert.derog_bit_english),
                               ("zone-a/mode-raw", convert.unit),
                               ("zone-a/mode-simple", convert.derog_bit_simple_english)]),
    18: TagDefinition("zone-a/temperature", convert.tenth),
    19: TagDefinition("zone-a/sensor-influence", convert.unit),
    20: TagDefinition("zone-a/curve", convert.tenth),
    21: TagDefinition("zone-a/calculated-temperature", convert.tenth),
    23: TagDefinition("zone-b/day-target-temperature", convert.tenth),
    24: TagDefinition("zone-b/night-target-temperature", convert.tenth),
    25: TagDefinition("zone-b/antifreeze-target-temperature", convert.tenth),
    26: MultipleTagDefinition([("zone-b/mode", convert.derog_bit_english),
                               ("zone-b/mode-raw", convert.unit),
                               ("zone-b/mode-simple", convert.derog_bit_simple_english)]),
    27: TagDefinition("zone-b/temperature", convert.tenth),
    28: TagDefinition("zone-b/sensor-influence", convert.unit),
    29: TagDefinition("zone-b/curve", convert.tenth),
    30: TagDefinition("zone-b/water-min-temperature", convert.tenth),
    31: TagDefinition("zone-b/water-max-temperature", convert.tenth),
    32: TagDefinition("zone-b/calculated-temperature", convert.tenth),
    33: TagDefinition("zone-b/water-temperature", convert.tenth),
    35: TagDefinition("zone-c/day-target-temperature", convert.tenth),
    36: TagDefinition("zone-c/night-target-temperature", convert.tenth),
    37: TagDefinition("zone-c/antifreeze-target-temperature", convert.tenth),
    38: MultipleTagDefinition([("zone-c/mode", convert.derog_bit_english),
                               ("zone-c/mode-raw", convert.unit),
                               ("zone-c/mode-simple", convert.derog_bit_simple_english)]),
    39: TagDefinition("zone-c/temperature", convert.tenth),
    40: TagDefinition("zone-c/sensor-influence", convert.unit),
    41: TagDefinition("zone-c/curve", convert.tenth),
    42: TagDefinition("zone-c/water-min-temperature", convert.tenth),
    43: TagDefinition("zone-c/water-max-temperature", convert.tenth),
    44: TagDefinition("zone-c/calculated-temperature", convert.tenth),
    45: TagDefinition("zone-c/water-temperature", convert.tenth),
    59: TagDefinition("dhw/target-temperature", convert.tenth),
    # TODO add specific convert
    60: TagDefinition("dhw/priority", convert.unit),
    61: TagDefinition("dhw/pump-postrun", convert.unit),
    62: TagDefinition("dhw/temperature", convert.tenth),
    64: TagDefinition("boiler/leading-boiler", convert.unit),
    68: TagDefinition("boiler/day-curve-footprint", convert.tenth),
    69: TagDefinition("boiler/night-curve-footprint", convert.tenth),
    70: TagDefinition("boiler/min-temperature", convert.tenth),
    71: TagDefinition("boiler/max-temperature", convert.tenth),
    72: TagDefinition("boiler/diff-a", convert.tenth),
    73: TagDefinition("boiler/diff-b", convert.tenth),
    74: TagDefinition("boiler/calculated-temperature", convert.tenth),
    75: TagDefinition("boiler/temperature", convert.tenth),
    76: TagDefinition("boiler/smoke-temp", convert.unit),
    77: TagDefinition("boiler/start-count-tenth", convert.unit),
    78: TagDefinition("boiler/hours-count-tenth", convert.unit),
    89: TagDefinition("boiler/base-ecs", convert.base_ecs),
    96: TagDefinition("dhw/night-target-temperature", convert.tenth),
    102: TagDefinition("outside/mean-temperature", convert.tenth),
    108: TagDefinition("boiler/date", convert.day_month_year, 3),
    113: TagDefinition("boiler/smoke-temp-inst", convert.unit),
    117: TagDefinition("boiler/temperature", convert.tenth),
    121: TagDefinition("dhw/target-temperature", convert.tenth),
    126: TagDefinition("zone-a/schedule-p4", convert.json_week_schedule, 21),
    147: TagDefinition("zone-b/schedule-p4", convert.json_week_schedule, 21),
    168: TagDefinition("zone-c/schedule-p4", convert.json_week_schedule, 21),
    189: TagDefinition("dhw/schedule", convert.json_week_schedule, 21),
    210: TagDefinition("zone-aux/schedule", convert.json_week_schedule, 21),
    231: TagDefinition("zone-a/program", convert.unit),
    232: TagDefinition("zone-b/program", convert.unit),
    233: TagDefinition("zone-c/program", convert.unit),
    247: TagDefinition("zone-a/autoadapt-shift", convert.tenth),
    248: TagDefinition("zone-b/autoadapt-shift", convert.tenth),
    249: TagDefinition("zone-c/autoadapt-shift", convert.tenth),
    251: TagDefinition("boiler/start-count-unit", convert.unit),
    252: TagDefinition("boiler/hours-count-unit", convert.unit),
    263: MultipleTagDefinition([("boiler/language", convert.language_english),
                                ("boiler/language-raw", convert.unit)]),
    264: TagDefinition("boiler/building-inertia", convert.unit),
    266: TagDefinition("boiler/bandwidth", convert.tenth),
    267: TagDefinition("boiler/3WV-shift", convert.tenth),
    269: TagDefinition("boiler/minimum-runing-time", convert.unit),
    271: TagDefinition("boiler/burner-temporisation", convert.unit),
    272: TagDefinition("boiler/pump-postrun", convert.unit),
    274: TagDefinition("outside/calibration", convert.tenth),
    275: TagDefinition("zone-a/calibration", convert.tenth),
    276: TagDefinition("zone-b/calibration", convert.tenth),
    277: TagDefinition("zone-c/calibration", convert.tenth),
    282: TagDefinition("zone-a/anticipation", convert.anticipation),
    283: TagDefinition("zone-b/anticipation", convert.anticipation),
    284: TagDefinition("zone-c/anticipation", convert.anticipation),
    289: TagDefinition("zone-a/day-curve-footprint", convert.footprint),
    290: TagDefinition("zone-a/night-curve-footprint", convert.footprint),
    291: TagDefinition("zone-b/day-curve-footprint", convert.footprint),
    292: TagDefinition("zone-b/night-curve-footprint", convert.footprint),
    296: TagDefinition("zone-a/zone-type", convert.zone_a_type_english),
    297: TagDefinition("zone-b/zone-type", convert.zone_bc_type_english),
    298: TagDefinition("zone-a/water-min-temperature", convert.tenth),
    299: TagDefinition("zone-a/water-max-temperature", convert.tenth),
    305: MultipleTagDefinition([("boiler/maximum-fan-speed", convert.fan),
                                ("boiler/maximum-fan-raw", convert.unit)]),
    307: MultipleTagDefinition([("boiler/fan-speed", convert.fan),
                                ("boiler/fan-raw", convert.unit)]),
    309: TagDefinition("schedule/day-begin-1", convert.day_month, 2),
    311: TagDefinition("schedule/day-end-1", convert.day_month, 2),
    313: TagDefinition("schedule/day-begin-2", convert.day_month, 2),
    315: TagDefinition("schedule/day-end-2", convert.day_month, 2),
    317: TagDefinition("schedule/day-begin-3", convert.day_month, 2),
    319: TagDefinition("schedule/day-end-3", convert.day_month, 2),
    321: TagDefinition("schedule/day-begin-4", convert.day_month, 2),
    323: TagDefinition("schedule/day-end-4", convert.day_month, 2),
    325: TagDefinition("schedule/day-begin-5", convert.day_month, 2),
    327: TagDefinition("schedule/day-end-5", convert.day_month, 2),
    329: TagDefinition("schedule/day-begin-6", convert.day_month, 2),
    331: TagDefinition("schedule/day-end-6", convert.day_month, 2),
    333: TagDefinition("schedule/day-begin-7", convert.day_month, 2),
    335: TagDefinition("schedule/day-end-7", convert.day_month, 2),
    337: TagDefinition("schedule/day-begin-8", convert.day_month, 2),
    339: TagDefinition("schedule/day-end-8", convert.day_month, 2),
    341: TagDefinition("schedule/day-begin-9", convert.day_month, 2),
    343: TagDefinition("schedule/day-end-9", convert.day_month, 2),
    345: TagDefinition("schedule/day-begin-10", convert.day_month, 2),
    347: TagDefinition("schedule/day-end-10", convert.day_month, 2),
    358: TagDefinition("zone-c/day-curve-footprint", convert.tenth),
    359: TagDefinition("zone-c/night-curve-footprint", convert.tenth),
    360: TagDefinition("zone-c/zone-type", convert.zone_bc_type_english),
    426: TagDefinition("boiler/boiler-3WV-temperature-shift", convert.tenth),
    436: TagDefinition("boiler/calculated-setpoint", convert.tenth),
    437: TagDefinition("boiler/pressure", convert.tenth),
    438: TagDefinition("boiler/3wv-bandwidth", convert.tenth),
    451: TagDefinition("boiler/ionization-current", convert.tenth),
    452: TagDefinition("boiler/temperature", convert.tenth),
    453: TagDefinition("boiler/return-temperature", convert.tenth),
    454: TagDefinition("boiler/smoke-temperature", convert.tenth),
    455: MultipleTagDefinition([("boiler/fan-speed", convert.fan),
                                ("boiler/fan-raw", convert.unit)]),
    456: TagDefinition("boiler/pressure", convert.tenth),
    457: TagDefinition("boiler/type", convert.unit),
    459: TagDefinition("dhw/temperature", convert.tenth),
    462: TagDefinition("boiler/calculated-temperature", convert.tenth),
    465: TagDefinition("boiler/error-code", convert.error_code),
    471: TagDefinition("boiler/power-inst", convert.tenth),
    472: TagDefinition("boiler/power-average", convert.tenth),
    473: TagDefinition("boiler/modulated-power", convert.unit),
    474: TagDefinition("boiler/output-state", convert.output_state, 2),
    480: TagDefinition("boiler/screen-text", convert.texte14, 7),
    507: TagDefinition("boiler/start-count", convert.unit_and_ten, 2),
    509: TagDefinition("boiler/hours-count", convert.unit_and_ten, 2),
    600: TagDefinition("boiler/version", convert.unit),
    601: TagDefinition("outside/temperature", convert.tenth),
    602: TagDefinition("boiler/temperature", convert.tenth),
    603: TagDefinition("dhw/temperature", convert.tenth),
    604: TagDefinition("boiler/smoke-temperature", convert.tenth),
    605: TagDefinition("zone-b/water-temperature", convert.tenth),
    606: TagDefinition("zone-c/water-temperature", convert.tenth),
    607: TagDefinition("boiler/return-temperature", convert.tenth),
    608: TagDefinition("boiler/ionization-current", convert.tenth),
    609: MultipleTagDefinition([("boiler/fan-speed", convert.fan),
                                ("boiler/fan-raw", convert.unit)]),
    610: TagDefinition("boiler/pressure", convert.tenth),
    614: TagDefinition("zone-a/temperature", convert.tenth),
    615: TagDefinition("zone-a/calculated-temperature", convert.tenth),
    616: TagDefinition("zone-b/temperature", convert.tenth),
    617: TagDefinition("zone-b/calculated-temperature", convert.tenth),
    618: TagDefinition("zone-c/temperature", convert.tenth),
    619: TagDefinition("zone-c/calculated-temperature", convert.tenth),
    620: TagDefinition("boiler/calculated-temperature", convert.tenth),
    622: TagDefinition("boiler/aux1-temperature", convert.tenth),
    623: TagDefinition("boiler/aux2-temperature", convert.tenth),
    624: TagDefinition("boiler/e-univ-temperature", convert.tenth),
    625: TagDefinition("boiler/exchange-temperature", convert.tenth),
    629: TagDefinition("boiler/average-flow-sensor-temperature", convert.tenth),
    634: TagDefinition("boiler/ten-volts-voltage-input", convert.tenth),
    637: TagDefinition("zone-a/active-mode", convert.active_mode_english),
    638: TagDefinition("zone-b/active-mode", convert.active_mode_english),
    639: TagDefinition("zone-c/active-mode", convert.active_mode_english),
    640: TagDefinition("dhw/active-mode", convert.active_mode_english),
    641: TagDefinition("zone-aux/active-mode", convert.active_mode_english),
    644: TagDefinition("boiler/active-mode", convert.boiler_mode_english),
    650: TagDefinition("zone-a/day-target-temperature", convert.tenth),
    651: TagDefinition("zone-a/night-target-temperature", convert.tenth),
    652: TagDefinition("zone-a/antifreeze-target-temperature", convert.tenth),
    653: MultipleTagDefinition([("zone-a/mode", convert.derog_bit_english),
                                ("zone-a/mode-raw", convert.unit),
                                ("zone-a/mode-simple", convert.derog_bit_simple_english)]),
    654: TagDefinition("zone-a/sensor-influence", convert.unit),
    655: TagDefinition("zone-a/curve", convert.tenth),
    656: TagDefinition("zone-b/day-target-temperature", convert.tenth),
    657: TagDefinition("zone-b/night-target-temperature", convert.tenth),
    658: TagDefinition("zone-b/antifreeze-target-temperature", convert.tenth),
    659: MultipleTagDefinition([("zone-b/mode", convert.derog_bit_english),
                                ("zone-b/mode-raw", convert.unit),
                                ("zone-b/mode-simple", convert.derog_bit_simple_english)]),
    660: TagDefinition("zone-b/sensor-influence", convert.unit),
    661: TagDefinition("zone-b/curve", convert.tenth),
    662: TagDefinition("zone-b/water-min-temperature", convert.tenth),
    663: TagDefinition("zone-b/water-max-temperature", convert.tenth),
    664: TagDefinition("zone-c/day-target-temperature", convert.tenth),
    665: TagDefinition("zone-c/night-target-temperature", convert.tenth),
    666: TagDefinition("zone-c/antifreeze-target-temperature", convert.tenth),
    667: MultipleTagDefinition([("zone-c/mode", convert.derog_bit_english),
                                ("zone-c/mode-raw", convert.unit),
                                ("zone-c/mode-simple", convert.derog_bit_simple_english)]),
    668: TagDefinition("zone-c/sensor-influence", convert.unit),
    669: TagDefinition("zone-c/curve", convert.tenth),
    670: TagDefinition("zone-c/water-min-temperature", convert.tenth),
    671: TagDefinition("zone-c/water-max-temperature", convert.tenth),
    672: TagDefinition("dhw/day-target-temperature", convert.tenth),
    673: TagDefinition("dhw/night-target-temperature", convert.tenth),
    674: TagDefinition("dhw/priority", convert.unit),
    677: TagDefinition("boiler/min-temperature", convert.tenth),
    678: TagDefinition("boiler/max-temperature", convert.tenth),
    679: TagDefinition("boiler/hours-minute", convert.hours_minutes, 2),
    681: TagDefinition("boiler/dayofweek", convert.unit),
    682: TagDefinition("boiler/date", convert.day_month_year, 3),
    686: TagDefinition("zone-b/swimming-pool-target-temperature", convert.tenth),
    687: TagDefinition("zone-c/swimming-pool-target-temperature", convert.tenth),
    707: TagDefinition("boiler/hp-state-bits", convert.hp_state_bit_english),
    708: TagDefinition("boiler/hp-state", convert.hp_state_english),
    710: TagDefinition("boiler/pcu-state", convert.unit),
    711: TagDefinition("boiler/pcu-substate", convert.unit),
    712: TagDefinition("boiler/pcu-block", convert.unit),
    713: TagDefinition("boiler/pcu-lock", convert.unit),
    721: TagDefinition("zone-a/antifreeze-duration", convert.unit),
    724: TagDefinition("zone-b/antifreeze-duration", convert.unit),
    727: TagDefinition("zone-c/antifreeze-duration", convert.unit),
    734: TagDefinition("boiler/second-calculated-temperature", convert.tenth),
    735: TagDefinition("boiler/state", convert.boiler_state_bit_english),
    741: TagDefinition("boiler/system-input-state", convert.system_input_state_english),
    744: TagDefinition("zone-aux/type", convert.zone_aux_type_english),
    770: TagDefinition("boiler/hours-minute", convert.hours_minutes, 2),
    772: TagDefinition("boiler/dayofweek", convert.unit),
    773: TagDefinition("boiler/date", convert.day_month_year, 3),
    788: TagDefinition("boiler/heating-power", convert.power, 3),
    791: TagDefinition("boiler/dhw-power", convert.power, 3),
    794: TagDefinition("boiler/cooling-power", convert.power, 3)


}

# Please note: only post to these MQTT topics for setting new values WITHOUT using MQTT's retain flag.
# Otherwise unexpected behavior occurs, e.g., on restarting the polling
# service or rebooting the machine.
WRITE_TABLE_MODULENS_O = {
    # "zone-a/antifreeze-duration/SET": WriteTagDefinition(13, convert.write_unit),
    "zone-a/program/SET": WriteTagDefinition(231, convert.write_unit),
    "zone-a/mode-simple/SET": WriteTagDefinition(653, convert.write_derog_bit_simple),
    "zone-a/mode-raw/SET": WriteTagDefinition(653, convert.write_unit),
    # antifreeze-duration do not work, boiler ignore value
    "zone-a/antifreeze-duration/SET": WriteTagDefinition(721, convert.write_unit),
    "zone-a/day-target-temperature/SET": WriteTagDefinition(650, convert.write_tenth),
    "zone-a/night-target-temperature/SET": WriteTagDefinition(651, convert.write_tenth),

    "zone-b/program/SET": WriteTagDefinition(232, convert.write_unit),
    "zone-b/mode-simple/SET": WriteTagDefinition(659, convert.write_derog_bit_simple),
    "zone-b/mode-raw/SET": WriteTagDefinition(659, convert.write_unit),
    "zone-b/antifreeze-duration/SET": WriteTagDefinition(724, convert.write_unit),
    "zone-b/day-target-temperature/SET": WriteTagDefinition(656, convert.write_tenth),
    "zone-b/night-target-temperature/SET": WriteTagDefinition(657, convert.write_tenth),
}

ZONE_TABLE_MODULENS_G = [(3,  3),
                         (59,  4),
                         (96,  1),
                         (102,  1),
                         (108,  3),
                         (231, 20),
                         (263,  1),
                         (309, 20),
                         (507,  4),
                         (465,  1),
                         (471, 10),
                         (600,  9),
                         (455,  1),
                         (610, 11),
                         (637, 24),
                         (681,  1),
                         (721,  4),
                         (788,  9), ]

# Please note: only post to these MQTT topics for setting new values WITHOUT using MQTT's retain flag.
# Otherwise unexpected behavior occurs, e.g., on restarting the polling
# service or rebooting the machine.
WRITE_TABLE_MODULENS_G = {
    "boiler/time-hours/SET": WriteTagDefinition(4, convert.write_unit),
    "boiler/time-minutes/SET": WriteTagDefinition(5, convert.write_unit),
    "boiler/language/SET": WriteTagDefinition(263, convert.write_language),
    "boiler/language-raw/SET": WriteTagDefinition(263, convert.write_unit),
    "zone-a/program/SET": WriteTagDefinition(231, convert.write_unit),
    "zone-a/mode-simple/SET": WriteTagDefinition(653, convert.write_derog_bit_simple),
    "zone-a/mode-raw/SET": WriteTagDefinition(653, convert.write_unit),
    # antifreeze-duration do not work, boiler ignore value
    "zone-a/antifreeze-duration/SET": WriteTagDefinition(721, convert.write_unit),
    "zone-a/day-target-temperature/SET": WriteTagDefinition(650, convert.write_tenth),
    "zone-a/night-target-temperature/SET": WriteTagDefinition(651, convert.write_tenth),

    "zone-b/program/SET": WriteTagDefinition(232, convert.write_unit),
    "zone-b/mode-simple/SET": WriteTagDefinition(659, convert.write_derog_bit_simple),
    "zone-b/mode-raw/SET": WriteTagDefinition(659, convert.write_unit),
    "zone-b/antifreeze-duration/SET": WriteTagDefinition(724, convert.write_unit),
    "zone-b/day-target-temperature/SET": WriteTagDefinition(656, convert.write_tenth),
    "zone-b/night-target-temperature/SET": WriteTagDefinition(657, convert.write_tenth),
}
