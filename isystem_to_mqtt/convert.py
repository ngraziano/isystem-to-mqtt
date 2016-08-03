""" Function to convert raw modbus value """


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
