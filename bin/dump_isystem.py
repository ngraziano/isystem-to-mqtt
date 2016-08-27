#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import time

import minimalmodbus

import isystem_to_mqtt.tables

parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Start adress default=0.", type=int, default=0)
parser.add_argument("--number", help="Number of word to read.", type=int, default=838)
parser.add_argument("--serial", help="Serial interface, default /dev/ttyUSB0",
                    default="/dev/ttyUSB0")
parser.add_argument("--deviceid", help="Modbus device id, default 10",
                    type=int, default=10)
parser.add_argument("--log", help="Logging level, default INFO",
                    default="INFO")
parser.add_argument("--bimaster", help="bi-master mode (5s for peer, 5s for us)",
                    action="store_true")
parser.add_argument("--model", help="boiler model",
                    default="modulens-o")
args = parser.parse_args()

# Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(args.log))
logging.basicConfig(level=numeric_level)

_LOGGER = logging.getLogger(__name__)


(READ_TABLE, WRITE_TABLE, READ_ZONES) = isystem_to_mqtt.tables.get_tables(args.model)



# Initialisation of Modbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
instrument = minimalmodbus.Instrument(args.serial, args.deviceid)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
# seconds (0.05 par defaut)
instrument.serial.timeout = 1
instrument.debug = False   # True or False
instrument.mode = minimalmodbus.MODE_RTU


# Bi master timeslot
# peer is master for 5s then we can be master for 5s
# timeout to 400ms

TIME_SLOT = 5
WAITING_TIMEOUT = 0.4

def wait_time_slot():
    """ In bi-master mode, wait for the 5s boiler is slave. """
    # if not in bimaster mode no need to wait
    if not args.bimaster:
        return

    # Wait a maximum of 3 cycle SLAVE => MASTER => SLAVE
    MAXIMUM_LOOP = 1 + int(TIME_SLOT * 3 / WAITING_TIMEOUT)
    instrument.serial.timeout = WAITING_TIMEOUT
    # read until boiler is master
    instrument.serial.open()
    data = b''
    number_of_wait = 0
    _LOGGER.debug("Wait the peer to be master.")
    #wait a maximum of 6 seconds
    while len(data) == 0 and number_of_wait < MAXIMUM_LOOP:
        data = instrument.serial.read(100)
        number_of_wait += 1
    if number_of_wait >= MAXIMUM_LOOP:
        _LOGGER.warning("Never get data from peer. Remove --bimaster flag.")
    # the master is the boiler wait for the end of data
    _LOGGER.debug("Wait the peer to be slave.")
    while len(data) != 0:
        data = instrument.serial.read(100)
    instrument.serial.close()
    instrument.serial.timeout = 1.0
    _LOGGER.debug("We are master.")
    # we are master for a maximum of  4.6s (5s - 400ms)

def read_zone(base_address, number_of_value):
    """ Read a MODBUS table zone and dump raw and converted. """
    try:
        raw_values = instrument.read_registers(base_address, number_of_value)
    except EnvironmentError:
        logging.exception("I/O error")
    except ValueError:
        logging.exception("Value error")
    else:
        for index in range(0, number_of_value):
            address = base_address + index
            print("{0:4d} => {1:5d} ".format(address, raw_values[index]), end='')
            tag_definition = READ_TABLE.get(address)
            if tag_definition:
                tag_definition.print(raw_values, index)
            print("")

wait_time_slot()

MAX_NUMBER_BY_READ = 123

# The total read time must be under the time slot duration
start_time = time.time()

for start_address in range(args.start, args.start + args.number, MAX_NUMBER_BY_READ):
    read_zone(start_address, min(MAX_NUMBER_BY_READ, args.start + args.number - start_address))

    duration = time.time() - start_time
    _LOGGER.debug("Read take %1.3fs", duration)
    if duration > TIME_SLOT-WAITING_TIMEOUT:
        wait_time_slot()
        start_time = time.time()


