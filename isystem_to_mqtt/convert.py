

def unit(raw_table, base_index):
    """ Direct word value """
    return raw_table[base_index]


def tenth(raw_table, base_index):
    """ Word value divide by ten """
    return raw_table[base_index] / 10


def unit_and_ten(raw_table, base_index):
    """ Two word values, xxxx0 and 0000x """
    return (raw_table[base_index] + 10 * raw_table[base_index + 1])

BIT_ANTIFREEZE = 1
BIT_NIGHT = 2
BIT_DAY = 4
BIT_AUTO = 8
BIT_DHW = 16
BIT_END_OF_PROGRAM = 32
BIT_DHW_END_OF_PROGRAM = 64
BIT_ALL_ZONE = 128

def derog_bit(raw_table, base_index):
    value = raw_table[base_index]
    stringvalue = ""
    if(value & BIT_ANTIFREEZE):
        stringvalue += "Antigel "
    if(value & BIT_NIGHT):
        stringvalue += "Nuit "
    if(value & BIT_DAY):
        stringvalue += "Jour "
    if(value & BIT_AUTO):
        stringvalue += "Automatique "
    if(value & BIT_DHW):
        stringvalue += "Eau "
    if(value & BIT_END_OF_PROGRAM):
        stringvalue += "jusqu'a la fin du programme "
    if(value & BIT_DHW_END_OF_PROGRAM):
        stringvalue += "jusqu'a la fin du programme (eau) "
    if(value & BIT_ALL_ZONE):
        stringvalue += "toutes les zones"
    return stringvalue



def write_unit(value):
    return [int(value)]

def write_tenth(value):
    return [int(value)*10]
