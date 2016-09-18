""" Function to convert raw modbus value """

import datetime
from . import time_delta_json

def unit(raw_table, base_index):
    """ Direct word value """
    return raw_table[base_index]


def tenth(raw_table, base_index):
    """ Word value divide by ten """
    raw_value = raw_table[base_index]
    if raw_value == 0xFFFF:
        return None
    sign = 1
    if raw_value & 0x8000:
        sign = -1
    return  sign * (raw_value & 0x7FFF) / 10


def unit_and_ten(raw_table, base_index):
    """ Two word values, 0000x and xxxx0 """
    return raw_table[base_index] + 10 * raw_table[base_index + 1]

BIT_ANTIFREEZE = 1
BIT_NIGHT = 2
BIT_DAY = 4
BIT_AUTO = 8
BIT_DHW = 16
BIT_END_OF_PROGRAM = 32
BIT_DHW_END_OF_PROGRAM = 64
BIT_ALL_ZONE = 128

def derog_bit(raw_table, base_index):
    """ Convert derog bit flag to french """
    value = raw_table[base_index]
    stringvalue = ""
    if value & BIT_ANTIFREEZE:
        stringvalue += "Antigel "
    if value & BIT_NIGHT:
        stringvalue += "Nuit "
    if value & BIT_DAY:
        stringvalue += "Jour "
    if value & BIT_AUTO:
        stringvalue += "Automatique "
    if value & BIT_DHW:
        stringvalue += "Eau "
    if value & BIT_END_OF_PROGRAM:
        stringvalue += "jusqu'a la fin du programme "
    if value & BIT_DHW_END_OF_PROGRAM:
        stringvalue += "jusqu'a la fin du programme (eau) "
    if value & BIT_ALL_ZONE:
        stringvalue += "toutes les zones"
    return stringvalue

def derog_bit_simple(raw_table, base_index):
    """ Convert derog bit flag to french do not handle all case """
    value = raw_table[base_index]
    stringvalue = ""
    if value & BIT_ANTIFREEZE:
        stringvalue = "Vacances"
    if value & BIT_NIGHT:
        stringvalue = "Nuit"
    if value & BIT_DAY:
        stringvalue = "Jour"
    if value & BIT_AUTO:
        stringvalue = "Automatique"
    return stringvalue

def active_mode(raw_table, base_index):
    """ Convert mode to french  """
    value = raw_table[base_index]
    if value == 0:
        return "Antigel"
    if value == 2:
        return "Nuit"
    if value == 4:
        return "Jour"
    return "Inconnu"

def boiler_mode(raw_table, base_index):
    """ Convert boiler mode to french  """
    value = raw_table[base_index]
    if value == 4:
        return "Ete"
    if value == 5:
        return "Hiver"
    return "Inconnu"

def day_schedule(raw_table, base_index):
    """ Convert schedule of present/away """
    current_mode = 0
    start_time = datetime.timedelta()
    current_time = datetime.timedelta()
    schedule = []
    interval_for_bit = datetime.timedelta(minutes=30)
    for word in raw_table[base_index:base_index + 3]:
        for _ in range(16):
            mode = word & 0x8000
            word <<= 1
            # end of period
            if mode == 0 and current_mode != 0:
                schedule.append((start_time, current_time))
                current_mode = mode

            current_time += interval_for_bit
            # before period
            if mode == 0:
                start_time = current_time

            current_mode = mode
    if current_mode != 0:
        schedule.append((start_time, current_time))

    return schedule

def json_week_schedule(raw_table, base_index):
    """ Convert week schedule to a JSON """
    schedule = {}
    for day in range(7):
        schedule[day] = day_schedule(raw_table, base_index + day * 3)
    encoder = time_delta_json.CustomDateJSONEncoder()
    return encoder.encode(schedule)

def hours_minutes_secondes(raw_table, base_index):
    """ Convert raw value to hours """
    return "%02d:%02d:%02d" % (raw_table[base_index],
                               raw_table[base_index+1],
                               raw_table[base_index+2])

def decrease(raw_table, base_index):
    """ Convert decrease flag to french """
    if raw_table[base_index] == 0:
        return "stop"
    else:
        return "abaissement"

def off_on(raw_table, base_index):
    """ Convert off/on flag to text """
    if raw_table[base_index] == 0:
        return "off"
    else:
        return "on"

def write_unit(value):
    """ Convert unit value to modbus value """
    return [int(value)]

def write_tenth(value):
    """ Convert tenth value to modbus value """
    int_value = int(float(value) * 10)
    if int_value < 0:
        int_value = abs(int_value) | 0x8000
    return [int_value]

DEROG_NAME_TO_VALUE = {
    "Vacances": BIT_ANTIFREEZE | BIT_END_OF_PROGRAM,
    "Nuit" : BIT_NIGHT | BIT_END_OF_PROGRAM,
    "Jour" : BIT_DAY | BIT_END_OF_PROGRAM,
    "Automatique" : BIT_AUTO
    }
def write_derog_bit_simple(value):
    """ Convert French Mode to bit value """
    if value not in DEROG_NAME_TO_VALUE:
        return None
    return [DEROG_NAME_TO_VALUE[value]]
