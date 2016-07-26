#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import queue
import logging
import ssl
import serial

import minimalmodbus
import paho.mqtt.client as mqtt

from isystem_to_mqtt.tables import READ_TABLE, WRITE_TABLE

parser = argparse.ArgumentParser()
parser.add_argument("server", help="MQtt server to connect to.")
parser.add_argument("--user", help="MQtt username.")
parser.add_argument("--password", help="MQtt password.")
parser.add_argument("--interval", help="Check interval default 60.", type=int, default=60)
parser.add_argument("--tls12", help="use TLS 1.2", dest="tls",
                    action="store_const", const=ssl.PROTOCOL_TLSv1_2)
parser.add_argument("--cacert", help="CA Certificate, default /etc/ssl/certs/ca-certificates.crt.",
                    default="/etc/ssl/certs/ca-certificates.crt")
parser.add_argument("--serial", help="Serial interface, default /dev/ttyUSB0",
                    default="/dev/ttyUSB0")
parser.add_argument("--deviceid", help="Modbus device id, default 10",
                    type=int, default=10)
parser.add_argument("--log", help="Logging level, default INFO",
                    default="INFO")
parser.add_argument("--bimaster", help="bi-master mode (5s for peer, 5s for us)",
                     action="store_true")
args = parser.parse_args()

# Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(args.log))
logging.basicConfig(level=numeric_level)

_LOGGER = logging.getLogger(__name__)


# Initialisation of mqtt client
base_topic = "heating/"

port_mqtt = 1883
client = mqtt.Client()
# client.on_log = on_log
if args.user:
    client.username_pw_set(args.user, args.password)
if args.tls:
    client.tls_set(args.cacert, tls_version=args.tls)
    port_mqtt = 8883

client.will_set(base_topic + "reading", "OFF", 1, True)

write_queue = queue.Queue()

def on_message(the_client, userdata, message):
    write_queue.put(message)

client.on_message = on_message

subscribe_list = [(base_topic + name, 0) for name in WRITE_TABLE.keys()]

def on_connect(the_client, userdata, flags, rc):
    if rc == mqtt.CONNACK_ACCEPTED:
        the_client.subscribe(subscribe_list)
        client.publish(base_topic + "reading", "ON", 1, True)

client.on_connect = on_connect

client.connect(args.server, port_mqtt)
client.loop_start()

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

serial_port = serial.Serial(port=args.serial,
                            baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE)
serial_port.close()

def wait_time_slot():
    # if not in bimaster mode no need to wait
    if not args.bimaster:
        return
    # peer is master for 5s then we can be master for 5s
    # timeout to 200ms
    serial_port.timeout = 0.2
    # read until boiler is master
    serial_port.open()
    data = b''
    number_of_wait = 0
    _LOGGER.debug("Wait the peer to be master.")
    #wait a maximum of 6 seconds
    while len(data) == 0 and number_of_wait < 30:
        data = serial_port.read(100)
        number_of_wait += 1
    if number_of_wait >= 30:
        _LOGGER.warning("Never get data from peer. Remove --bimaster flag.")
    # the master is the boiler wait for the end of data
    _LOGGER.debug("Wait the peer to be slave.")
    while len(data) != 0:
        data = serial_port.read(10)
    serial_port.close()
    _LOGGER.debug("We are master.")
    # we are master for a maximum of  4.8s (5s - 200ms)

def read_zone(base_address, number_of_value):
    try:
        raw_values = instrument.read_registers(base_address, number_of_value)
    except EnvironmentError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    else:
        for index in range(0, number_of_value):
            address = base_address + index
            tag_definition = READ_TABLE.get(address)
            if tag_definition:
                tag_definition.publish(client, base_topic, raw_values, index)

def write_value(message):
    tag_definition = WRITE_TABLE.get(message.topic.strip(base_topic))
    if tag_definition:
        value = tag_definition.convertion(message.payload)
        print("write value {} : add : {} = {}".format(message.topic.strip(base_topic), tag_definition.address, value))
        instrument.write_registers(tag_definition.address, value)


wait_time_slot()

# Main loop
while True:
    read_zone(600, 21)
    read_zone(507, 4)
    read_zone(650, 10)
    read_zone(231, 1)
    read_zone(721, 1)
    # Traitement de toute les ecritures ou attente de l'intervale
    try:
        waittime = args.interval
        while True:
            writeelement = write_queue.get(timeout=waittime)
           
            wait_time_slot()
            write_value(writeelement)
            waittime = 0
    except queue.Empty:
        wait_time_slot()
        continue

