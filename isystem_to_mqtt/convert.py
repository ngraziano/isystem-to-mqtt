""" Function to convert raw modbus value """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import json
from . import time_delta_json


def unit(raw_table, base_index):
    """ Direct word value """
    raw_value = raw_table[base_index]
    sign = 1
    if raw_value & 0x8000:
        sign = -1
    return sign * (raw_value & 0x7FFF)


def tenth(raw_table, base_index):
    """ Word value divide by ten """
    raw_value = raw_table[base_index]
    if raw_value == 0xFFFF:
        return None
    sign = 1
    if raw_value & 0x8000:
        sign = -1
    return sign * (raw_value & 0x7FFF) / 10


def unit_and_ten(raw_table, base_index):
    """ Two word values, 0000x and xxxx0 """
    return raw_table[base_index] + 10 * raw_table[base_index + 1]


def anticipation(raw_table, base_index):
    """ 101 for None or value divide by ten """
    raw_value = raw_table[base_index]
    if raw_value == 101:
        return None
    return tenth(raw_table, base_index)


def footprint(raw_table, base_index):
    """ 150 for None or value divide by ten """
    raw_value = raw_table[base_index]
    if raw_value == 150:
        return None
    return tenth(raw_table, base_index)


def power(raw_table, base_index):
    """ Value of MWh, KWh, Wh or None if 65535 """
    if (raw_table[base_index] == 0xFFFF
            or raw_table[base_index + 1] == 0xFFFF
            or raw_table[base_index + 2] == 0xFFFF):
        return None
    return (raw_table[base_index] * 1000 + raw_table[base_index + 1]) * 1000 + raw_table[base_index + 2]

BIT_ANTIFREEZE = 1
BIT_NIGHT = 2
BIT_DAY = 4
BIT_AUTO = 8
BIT_DHW = 16
BIT_END_OF_PROGRAM = 32
BIT_DHW_END_OF_PROGRAM = 64
BIT_ALL_ZONE = 128


def derog_bit_french(raw_table, base_index):
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


def derog_bit_english(raw_table, base_index):
    """ Convert derog bit flag to English """
    value = raw_table[base_index]
    stringvalue = ""
    if value & BIT_ANTIFREEZE:
        stringvalue += "Antifreeze/vacation "
    if value & BIT_NIGHT:
        stringvalue += "Night "
    if value & BIT_DAY:
        stringvalue += "Day "
    if value & BIT_AUTO:
        stringvalue += "Automatic "
    if value & BIT_DHW:
        stringvalue += "Water "
    if value & BIT_END_OF_PROGRAM:
        stringvalue += "until the end of program "
    if value & BIT_DHW_END_OF_PROGRAM:
        stringvalue += "until the end of program (warm water) "
    if value & BIT_ALL_ZONE:
        stringvalue += "all zones"
    return stringvalue


def derog_bit_simple_french(raw_table, base_index):
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


def derog_bit_simple_english(raw_table, base_index):
    """ Convert derog bit flag to English do not handle all case """
    value = raw_table[base_index]
    stringvalue = ""
    if value & BIT_ANTIFREEZE:
        stringvalue = "Vacation"
    if value & BIT_NIGHT:
        stringvalue = "Night"
    if value & BIT_DAY:
        stringvalue = "Day"
    if value & BIT_AUTO:
        stringvalue = "Automatic"
    return stringvalue


def boiler_state_bit_english(raw_table, base_index):
    """ Convert derog bit flag to English """
    value = raw_table[base_index]
    stringvalue = ""
    if value & (1 << 1):
        stringvalue += "[Direct Circuit OFF] "
    if value & (1 << 2):
        stringvalue += "[3WV Circuit OFF] "
    if value & (1 << 3):
        stringvalue += "[Secondary pump] "
    if value & (1 << 15):
        stringvalue += "[Cascade faliure] "
    return stringvalue


def hp_state_english(raw_table, base_index):
    """ Convert HP state to English  """
    value = raw_table[base_index]
    if value == 0:
        return "Stop"
    if value == 1:
        return "Heating mode"
    if value == 2:
        return "Heating mode+comp"
    if value == 4:
        return "Cooling mode"
    if value == 5:
        return "Cooling mode+comp on"
    return "Unknown"


def hp_state_bit_english(raw_table, base_index):
    """ Convert derog bit flag to English """
    value = raw_table[base_index]
    stringvalue = ""
    if value & (1 << 1):
        stringvalue += "[Defrosting] "
    if value & (1 << 1):
        stringvalue += "[Boiler Pump Backup] "
    if value & (1 << 1):
        stringvalue += "[Boiler Backup] "
    if value & (1 << 1):
        stringvalue += "[HP Pump] "
    if value & (1 << 1):
        stringvalue += "[Backup 2] "
    if value & (1 << 1):
        stringvalue += "[Backup 1] "
    if value & (1 << 1):
        stringvalue += "[Compressor] "
    return stringvalue


def system_input_state_english(raw_table, base_index):
    """ Convert system input state to English  """
    value = raw_table[base_index]
    if value == 0:
        return "Disable"
    if value == 1:
        return "System"
    if value == 2:
        return "Storage tank"
    if value == 3:
        return "DHW STRAT"
    if value == 4:
        return "Storage tank+ DHW"
    return "Unknown"


def zone_aux_type_english(raw_table, base_index):
    """ Convert zone aux type to English  """
    value = raw_table[base_index]
    if value == 0:
        return "NA"
    if value == 1:
        return "NA"
    if value == 2:
        return "NA"
    if value == 3:
        return "DHW loop"
    if value == 4:
        return "NA"
    if value == 5:
        return "Program"
    if value == 8:
        return "primary pump"
    if value == 9:
        return "burner command"
    if value == 11:
        return "DHW"
    if value == 13:
        return "failure"
    if value == 15:
        return "Electrical DHW"
    if value == 17:
        return "VM pump"
    if value == 18:
        return "cascade failure"
    return "Unknown"


def active_mode_french(raw_table, base_index):
    """ Convert mode to french  """
    value = raw_table[base_index]
    if value == 0:
        return "Antigel"
    if value == 2:
        return "Nuit"
    if value == 4:
        return "Jour"
    return "Inconnu"


def active_mode_english(raw_table, base_index):
    """ Convert mode to English  """
    value = raw_table[base_index]
    if value == 0:
        return "Vacation"
    if value == 2:
        return "Night"
    if value == 4:
        return "Day"
    return "Unknown"


def boiler_mode_french(raw_table, base_index):
    """ Convert boiler mode to french  """
    value = raw_table[base_index]
    if value == 4:
        return "Ete"
    if value == 5:
        return "Hiver"
    return "Inconnu"


def boiler_mode_english(raw_table, base_index):
    """ Convert boiler mode to french  """
    value = raw_table[base_index]
    if value == 4:
        return "Summer"
    if value == 5:
        return "Winter"
    return "Unknown"


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


def zone_a_type_english(raw_table, base_index):
    """ Convert zone b type to English  """
    value = raw_table[base_index]
    if value == 0:
        return "Disable"
    if value == 1:
        return "Direct"
    if value == 2:
        return "NA"
    if value == 3:
        return "NA"
    if value == 4:
        return "NA"
    if value == 5:
        return "Program"
    if value == 6:
        return "NA"
    if value == 7:
        return "H.temp"
    if value == 8:
        return "NA"
    if value == 9:
        return "NA"
    if value == 10:
        return "NA"
    if value == 11:
        return "DHW"
    if value == 12:
        return "NA"
    if value == 13:
        return "NA"
    if value == 14:
        return "NA"
    if value == 15:
        return "Electrical DHW"
    return "Unknown"


def zone_bc_type_english(raw_table, base_index):
    """ Convert zone b/c type to English  """
    value = raw_table[base_index]
    if value == 0:
        return "NA"
    if value == 1:
        return "Direct"
    if value == 2:
        return "3WV"
    if value == 3:
        return "NA"
    if value == 4:
        return "swiming pool"
    return "Unknown"


def error_code(raw_table, base_index):
    """ Convert error codes """
    value = raw_table[base_index]
    if value == 0x0000:
        return "D3:OUTL S.B FAIL."
    if value == 0x0001:
        return "D4:OUTL S.C FAIL."
    if value == 0x0002:
        return "D5:OUTSI.S.FAIL."
    if value == 0x0003:
        return "D7:SYST.SENS.FAIL."
    if value == 0x0004:
        return "D9:DHW S.FAILURE"
    if value == 0x0005:
        return "D11:ROOM S.A FAIL."
    if value == 0x0006:
        return "D12:ROOM S.B FAIL."
    if value == 0x0007:
        return "D13:ROOM S.C FAIL."
    if value == 0x0008:
        return "D14:MC COM.FAIL"
    if value == 0x0009:
        return "D15:ST.TANK S.FAIL"
    if value == 0x000A:
        return "D16:SWIM.P.B.S.FA"
    if value == 0x000B:
        return "D16:SWIM.P.C.S.FA"
    if value == 0x000C:
        return "D17:DHW 2 S.FAIL"
    if value == 0x000D:
        return "D27:PCU COM.FAIL"
    if value == 0x000E:
        return "Not Available"
    if value == 0x000F:
        return "Not Available"
    if value == 0x0010:
        return "Not Available"
    if value == 0x0011:
        return "Not Available"
    if value == 0x0012:
        return "D32:5 RESET:ON/OFF"
    if value == 0x0013:
        return "D37:TA-S SHORT-CIR"
    if value == 0x0014:
        return "D38:TA-S DISCONNEC"
    if value == 0x0015:
        return "D39:TA-S FAILURE"
    if value == 0x0016:
        return "D50:OTH COM.FAIL"
    if value == 0x0017:
        return "D51:DEF :SEE BOILER"
    if value == 0x0018:
        return "D18:SOL.HW S.FAIL"
    if value == 0x0019:
        return "D19:SOL.COL.S.FAIL"
    if value == 0x001A:
        return "D20:SOL COM.FAIL"
    if value == 0x001B:
        return "D99:DEF.BAD PCU"
    if value == 0x001C:
        return "D40:FAIL UNKNOWN"
    if value == 0x001D:
        return "D254:FAIL UNKNOWN"

    if value == 0x800:
        return "B0:PSU FAIL"
    if value == 0x801:
        return "B1:PSU PARAM FAIL"
    if value == 0x802:
        return "B2:EXCHAN.S.FAIL"
    if value == 0x803:
        return "B3:EXCHAN.S.FAIL"
    if value == 0x804:
        return "B4:EXCHAN.S.FAIL"
    if value == 0x805:
        return "B5:STB EXCHANGE"
    if value == 0x806:
        return "B6:BACK S.FAILURE"
    if value == 0x807:
        return "B7:BACK S.FAILURE"
    if value == 0x808:
        return "B8:BACK S.FAILURE"
    if value == 0x809:
        return "B9:STB BACK"
    if value == 0x80A:
        return "B10:DT.EXCH.BAC.FAIL"
    if value == 0x80B:
        return "B11:DT.BAC.EXCH.FAIL"
    if value == 0x80C:
        return "B12:STB OPEN"
    if value == 0x80D:
        return "B14:BURNER FAILURE"
    if value == 0x80E:
        return "B15:CCE.TST.FAIL"
    if value == 0x80F:
        return "B16:PARASIT FLAME"
    if value == 0x810:
        return "B17:VALVE FAIL"
    if value == 0x811:
        return "B32:DEF.OUTLET S."
    if value == 0x812:
        return "B33:DEF.OUTLET S."
    if value == 0x813:
        return "B34:FAN FAILURE"
    if value == 0x814:
        return "B35:BACK>BOIL FAIL"
    if value == 0x815:
        return "B36:I-CURRENT FAIL"
    if value == 0x816:
        return "B37:SU COM.FAIL"
    if value == 0x817:
        return "B38:PCU COM.FAIL"
    if value == 0x818:
        return "B39:BL OPEN FAIL"
    if value == 0x819:
        return "B255:FAIL UNKNOWN"
    if value == 0x81A:
        return "B254:FAIL UNKNOWN"

    if value == 0x1000:
        return "DEF.PSU 00"
    if value == 0x1001:
        return "DEF.PSU PARAM 01"
    if value == 0x1002:
        return "DEF.S.DEPART 02"
    if value == 0x1003:
        return "DEF.S.DEPART 03"
    if value == 0x1004:
        return "DEF.S.DEPART 04"
    if value == 0x1005:
        return "STB DEPART 05"
    if value == 0x1006:
        return "DEF.S.RETOUR 06"
    if value == 0x1007:
        return "DEF.S.RETOUR 07"
    if value == 0x1008:
        return "DEF.S.RETOUR 08"
    if value == 0x1009:
        return "STB RETOUR 09"
    if value == 0x100A:
        return "DT.DEP-RET<MIN 10"
    if value == 0x100B:
        return "DT.DEP-RET>MAX 11"
    if value == 0x100C:
        return "STB OUVERT 12"
    if value == 0x100D:
        return "DEF.ALLUMAGE 14"
    if value == 0x100E:
        return "FLAM.PARASI. 16"
    if value == 0x100F:
        return "DEF.VANNE GAZ 17"
    if value == 0x1010:
        return "DEF.VENTILO 34"
    if value == 0x1011:
        return "DEF.RET>CHAUD 35"
    if value == 0x1012:
        return "DEF.IONISATION 36"
    if value == 0x1013:
        return "DEF.COM.SU 37"
    if value == 0x1014:
        return "DEF.COM PCU 38"
    if value == 0x1015:
        return "DEF BL OUVERT 39"
    if value == 0x1016:
        return "DEF.TEST.HRU 40"
    if value == 0x1017:
        return "DEF.MANQUE EAU 250"
    if value == 0x1018:
        return "DEF.MANOMETRE 251"
    if value == 0x1019:
        return "DEF.INCONNU 255"
    if value == 0x101A:
        return "DEF.INCONNU 254"

    if value == 0x1800:
        return "L0:PSU FAIL"
    if value == 0x1801:
        return "L1:PSU PARAM FAIL"
    if value == 0x1802:
        return "L2:STB OUTLET"
    if value == 0x1803:
        return "L3:DEF.OIL.SENSOR"
    if value == 0x1804:
        return "L4:BURNER FAILURE"
    if value == 0x1805:
        return "L5:DEF.INTERNAL"
    if value == 0x1806:
        return "L6:DEF.SPEED.MOT"
    if value == 0x1807:
        return "L7:DEF.T.WARM UP"
    if value == 0x1808:
        return "L8:DEF.PAR.FLAME"
    if value == 0x1809:
        return "L9:OIL.PRES FAIL."
    if value == 0x180A:
        return "L30:SMOKE PRE.FAIL"
    if value == 0x180B:
        return "L31:DEF.SMOKE.TEMP"
    if value == 0x180C:
        return "L32:DEF.OUTLET S."
    if value == 0x180D:
        return "L33:DEF.OUTLET S."
    if value == 0x180E:
        return "L34:BACK S.FAILURE"
    if value == 0x180F:
        return "L35:BACK S.FAILURE"
    if value == 0x1810:
        return "L36:DEF.FLAME LOS"
    if value == 0x1811:
        return "L37:SU COM.FAIL"
    if value == 0x1812:
        return "L38:PCU COM.FAIL"
    if value == 0x1813:
        return "L39:BL OPEN FAIL"
    if value == 0x1814:
        return "L250:DEF.WATER MIS."
    if value == 0x1815:
        return "L251:MANOMETRE FAIL"
    if value == 0x1816:
        return "L255:FAIL UNKNOWN"
    if value == 0x1817:
        return "L254:FAIL UNKNOWN"

    if value == 0x2000:
        return "L1:DEF.COMP.PAC"
    if value == 0x2001:
        return "L2:DEF.V4V PAC"
    if value == 0x2002:
        return "L3:DEF.POMPE PAC"
    if value == 0x2003:
        return "L4:PAC HORS LIMIT"
    if value == 0x2004:
        return "L5:DEF.DEB.PAC 6"
    if value == 0x2005:
        return "L6:DEF.DEB.PAC 8"
    if value == 0x2006:
        return "L7:DEF.COM.PAC"
    if value == 0x2007:
        return "L8:DEF.S.SOR.COMP"
    if value == 0x2008:
        return "L9:DEF.H.P PAC"
    if value == 0x2009:
        return "L10:DEF.B.P PAC"
    if value == 0x200A:
        return "L11:DEF.PRES.SOURC"
    if value == 0x200B:
        return "L12:DEF.ANTI.SOUR."
    if value == 0x200C:
        return "L13:DEF.P.SOURCE"
    if value == 0x200D:
        return "L14:DEF.ANTI.COND."
    if value == 0x200E:
        return "L15:DEF.DEGIVRAGE"
    if value == 0x200F:
        return "L16:DEF.PROT.MOT."
    if value == 0x2010:
        return "L17:DEF.S.GAZ.CH."
    if value == 0x2011:
        return "L18:DEF.COM.PAC"
    if value == 0x2012:
        return "L19:DEF.S.DEP.PAC"
    if value == 0x2013:
        return "L20:DEF.S.RET.PAC"
    if value == 0x2014:
        return "L21:DEF.S.EXT.ENT."
    if value == 0x2015:
        return "L22:DEF.S.EXT.SOR."
    if value == 0x2016:
        return "L23:DEF.S.GAZ EXP."
    if value == 0x2017:
        return "L24:DEF.S.EVAPO."
    if value == 0x2018:
        return "L25:DEF.S.CONDENS."
    if value == 0x2019:
        return "L32:BL.USER.RESET"
    if value == 0x201A:
        return "L33:DEF.DEBIT"
    if value == 0x201B:
        return "L255:DEF.INCONNU"
    if value == 0x201C:
        return "L254:DEF.INCONNU"

    if value == 0xFFFF:
        return "no error"
    return "Unknown"


def language_english(raw_table, base_index):
    """ Convert language name to English  """
    value = raw_table[base_index]
    if value == 0:
        return "French"
    if value == 1:
        return "German"
    if value == 2:
        return "English"
    if value == 3:
        return "Italian"
    if value == 4:
        return "Spanish"
    if value == 5:
        return "Dutch"
    if value == 6:
        return "Polish"
    if value == 7:
        return "Turkish"
    if value == 8:
        return "Russian"
    return "Unknown"


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
                               raw_table[base_index + 1],
                               raw_table[base_index + 2])


def hours_minutes(raw_table, base_index):
    """ Convert raw value to hours """
    return "%02d:%02d" % (raw_table[base_index],
                          raw_table[base_index + 1])


def day_month(raw_table, base_index):
    """ Convert raw value to date """
    return "%02d/%02d" % (raw_table[base_index],
                          raw_table[base_index + 1])


def day_month_year(raw_table, base_index):
    """ Convert raw value to date """
    return "%02d/%02d/%02d" % (raw_table[base_index],
                               raw_table[base_index + 1],
                               raw_table[base_index + 2])


def decrease_french(raw_table, base_index):
    """ Convert decrease flag to french """
    if raw_table[base_index] == 0:
        return "stop"
    else:
        return "abaissement"


def decrease_english(raw_table, base_index):
    """ Convert decrease flag to french """
    if raw_table[base_index] == 0:
        return "stop"
    else:
        return "decreasing"


def off_on(raw_table, base_index):
    """ Convert off/on flag to text """
    if raw_table[base_index] == 0:
        return "off"
    else:
        return "on"

OUTPUT1_BURNER = 3
OUTPUT1_HYDRAULIC_VALVE_OPEN = 1 << 2
OUTPUT1_HYDRAULIC_VALVE_CLOSE = 1 << 3
OUTPUT1_BOILER_PUMP = 1 << 4
# It's ON on my boiler, I want to follow it.
OUTPUT1_UNKNOW1 = 1 << 5

OUTPUT2_DHW_PUMP = 1 << 0
OUTPUT2_ZONEA_PUMP = 1 << 1
OUTPUT2_ZONEB_PUMP = 1 << 4
OUTPUT2_ZONEB_3WV_OPEN = 1 << 5
OUTPUT2_ZONEB_3WV_CLOSE = 1 << 6
OUTPUT2_ZONEC_PUMP = 1 << 7
OUTPUT2_ZONEC_3WV_OPEN = 1 << 8
OUTPUT2_ZONEC_3WV_CLOSE = 1 << 9
OUTPUT2_AUX_PUMP = 1 << 10


def output_state(raw_table, base_index):
    """ Convert output state to JSON """
    result = {}
    val = raw_table[base_index]
    result["burner"] = val & OUTPUT1_BURNER
    result["hydraulic_valve_open"] = bool(val & OUTPUT1_HYDRAULIC_VALVE_OPEN)
    result["hydraulic_valve_close"] = bool(val & OUTPUT1_HYDRAULIC_VALVE_CLOSE)
    result["hydraulic_boiler_pump"] = bool(val & OUTPUT1_BOILER_PUMP)
    result["UNKNOWN1"] = bool(val & OUTPUT1_UNKNOW1)
    val = raw_table[base_index + 1]
    result["DHW_pump"] = bool(val & OUTPUT2_DHW_PUMP)
    result["zone_A_pump"] = bool(val & OUTPUT2_ZONEA_PUMP)
    result["zone_B_pump"] = bool(val & OUTPUT2_ZONEB_PUMP)
    result["zone_B_3WV_open"] = bool(val & OUTPUT2_ZONEB_3WV_OPEN)
    result["zone_B_3WV_close"] = bool(val & OUTPUT2_ZONEB_3WV_CLOSE)
    result["zone_C_pump"] = bool(val & OUTPUT2_ZONEC_PUMP)
    result["zone_C_3WV_open"] = bool(val & OUTPUT2_ZONEC_3WV_OPEN)
    result["zone_C_3WV_close"] = bool(val & OUTPUT2_ZONEC_3WV_CLOSE)
    result["AUX_pump"] = bool(val & OUTPUT2_AUX_PUMP)
    return json.dumps(result)

BASEECS_AUX_PUMP = 1
BASEECS_ZONEA_PUMP_BOILER = 1 << 1
BASEECS_BURNER_1_2 = 1 << 2
BASEECS_BURNER_1_1 = 1 << 3
BASEECS_ZONEA_PUMP = 1 << 4
BASEECS_DHW_PUMP = 1 << 5
BASEECS_ALARM_BURNER = 1 << 6
# BASEECS_ = 1 << 7
BASEECS_VALVE = 1 << 8


def base_ecs(raw_table, base_index):
    """ Convert base_ecs state to JSON """
    result = {}
    val = raw_table[base_index]
    result["AUX_pump"] = bool(val & BASEECS_AUX_PUMP)
    result["zone_A_pump_boiler"] = bool(val & BASEECS_ZONEA_PUMP_BOILER)
    result["burner_1_2"] = bool(val & BASEECS_BURNER_1_2)
    result["burner_1_1"] = bool(val & BASEECS_BURNER_1_1)
    result["zone_A_pump"] = bool(val & BASEECS_ZONEA_PUMP)
    result["DHW_pump"] = bool(val & BASEECS_DHW_PUMP)
    result["Alarm_burner"] = bool(val & BASEECS_ALARM_BURNER)
    result["valve"] = bool(val & BASEECS_VALVE)

    return json.dumps(result)


def fan(raw_table, base_index):
    """ Convert for fan speed """
    val = raw_table[base_index]
    return val & 0x007F


def texte14(raw_table, base_index):
    """ Convert 14 char of text """
    result = ''
    for word in raw_table[base_index:base_index + 7]:
        result = result + chr(word >> 8) + chr(word & 0x00FF)
    return result


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
    "Nuit": BIT_NIGHT | BIT_END_OF_PROGRAM,
    "Jour": BIT_DAY | BIT_END_OF_PROGRAM,
    "Automatique": BIT_AUTO,
    "Vacation": BIT_ANTIFREEZE | BIT_END_OF_PROGRAM,
    "Night": BIT_NIGHT | BIT_END_OF_PROGRAM,
    "Day": BIT_DAY | BIT_END_OF_PROGRAM,
    "Automatic": BIT_AUTO
}


def write_derog_bit_simple(value):
    """ Convert French Mode to bit value """
    if value not in DEROG_NAME_TO_VALUE:
        return None
    return [DEROG_NAME_TO_VALUE[value]]

LANGUAGE_NAME_TO_VALUE = {
    "French": 0,
    "German": 1,
    "English": 2,
    "Italian": 3,
    "Spanish": 4,
    "Dutch": 5,
    "Polish": 6,
    "Turkish": 7,
    "Russian": 8
}


def write_language(value):
    """ Convert French Mode to bit value """
    if value not in LANGUAGE_NAME_TO_VALUE:
        return None
    return [LANGUAGE_NAME_TO_VALUE[value]]
