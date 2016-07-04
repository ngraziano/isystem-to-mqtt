

def unit(raw_table, base_index):
    return raw_table[base_index]


def tenth(raw_table, base_index):
    return raw_table[base_index] / 10


def unit_and_ten(raw_table, base_index):
    return (raw_table[base_index] + 10 * raw_table[base_index + 1])



def write_unit(value):
    return [int(value)]

def write_tenth(value):
    return [int(value)*10]
