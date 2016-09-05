""" specialized version of modbus for isystem with
master mode """

import logging

from minimalmodbus import Instrument, serial, MODE_RTU

_LOGGER = logging.getLogger(__name__)

# Bi master timeslot
# peer is master for 5s then we can be master for 5s
# timeout to 400ms

TIME_SLOT = 5
WAITING_TIMEOUT = 0.4
# Wait a maximum of 3 cycle SLAVE => MASTER => SLAVE
MAXIMUM_LOOP = 1 + int(TIME_SLOT * 3 / WAITING_TIMEOUT)
MAXIMUM_OPERATION = TIME_SLOT - WAITING_TIMEOUT

class ISystemInstrument(Instrument):
    """ Modbus instrument dedicated to Isystem """
    def __init__(self, port, slaveaddress, bimaster=False):
        Instrument.__init__(self, port, slaveaddress)
        self.serial.baudrate = 9600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 1
        self.mode = MODE_RTU
        self.bimaster = bimaster


    def wait_time_slot(self):
        """ In bi-master mode, wait for the 5s boiler is slave. """
        # if not in bimaster mode no need to wait
        if not self.bimaster:
            return

        self.serial.timeout = WAITING_TIMEOUT
        # read until boiler is master
        self.serial.open()
        data = b''
        number_of_wait = 0
        _LOGGER.debug("Wait the peer to be master.")
        #wait a maximum of 6 seconds
        while len(data) == 0 and number_of_wait < MAXIMUM_LOOP:
            data = self.serial.read(100)
            number_of_wait += 1
        if number_of_wait >= MAXIMUM_LOOP:
            _LOGGER.warning("Never get data from peer. Remove --bimaster flag.")
        # the master is the boiler wait for the end of data
        _LOGGER.debug("Wait the peer to be slave.")
        while len(data) != 0:
            data = self.serial.read(100)
        self.serial.close()
        self.serial.timeout = 1.0
        _LOGGER.debug("We are master.")
        # we are master for a maximum of  4.6s (5s - 400ms)

