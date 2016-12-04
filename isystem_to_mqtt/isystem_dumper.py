""" Class to dump ISystem values to stdout """

import logging
import time

import minimalmodbus

from . import isystem_modbus
from . import tables

_LOGGER = logging.getLogger(__name__)

# Limit from Modbus protocol
MAX_NUMBER_BY_READ = 123

class ISystemDumper(object):
    def __init__(self, parameters):
        self.parameters = parameters
        (self.read_table,
         self.write_table,
         self.read_zones) = tables.get_tables(self.parameters.model)
        # Initialisation of Modbus
        minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
        self.instrument = isystem_modbus.ISystemInstrument(self.parameters.serial,
                                                           self.parameters.deviceid,
                                                           self.parameters.bimaster)
        self.instrument.debug = False   # True or False



    def read_zone(self, base_address, number_of_value):
        """ Read a MODBUS table zone and dump raw and converted. """
        try:
            raw_values = self.instrument.read_registers(base_address, number_of_value)
        except EnvironmentError:
            logging.exception("I/O error")
        except ValueError:
            logging.exception("Value error")
        else:
            next_not_used_adress = 0
            for index in range(0, number_of_value):
                address = base_address + index
                print("{0:4d} => {1:5d} ".format(address, raw_values[index]), end='')
                tag_definition = self.read_table.get(address)
                if tag_definition:
                    tag_definition.print(raw_values, index)
                    next_not_used_adress = max(
                        next_not_used_adress,
                        address + tag_definition.needed_value)
                else:
                    if address < next_not_used_adress:
                        print("^", end='')
                print("")

    def dump_system(self, start, number):
        """ dump isystem value from start adress for number of address """
        self.instrument.wait_time_slot()
        # The total read time must be under the time slot duration
        start_time = time.time()

        for start_address in range(start, start + number, MAX_NUMBER_BY_READ):
            self.read_zone(
                start_address,
                min(MAX_NUMBER_BY_READ, start + number - start_address))

            duration = time.time() - start_time
            _LOGGER.debug("Read take %1.3fs", duration)
            if duration > isystem_modbus.MAXIMUM_OPERATION:
                self.instrument.wait_time_slot()
                start_time = time.time()

