#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import logging
import time

try:
    import queue
except ImportError:
    import Queue as queue

import minimalmodbus
import paho.mqtt.client as mqtt

import isystem_to_mqtt.tables
import isystem_to_mqtt.isystem_modbus

parser = argparse.ArgumentParser()
parser.add_argument("server", help="MQtt server to connect to.")
parser.add_argument("--user", help="MQtt username.")
parser.add_argument("--password", help="MQtt password.")
parser.add_argument("--interval", help="Check interval default 60s.", type=int, default=60)
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
parser.add_argument("--model", help="boiler model",
                    default="modulens-o")
parser.add_argument("--lang", help="language in mqtt message",
                    default="en")
# handle no sll.PROTOCOL_TLSv1_2
try:
    import ssl
    parser.add_argument("--tls12", help="use TLS 1.2", dest="tls",
                        action="store_const", const=ssl.PROTOCOL_TLSv1_2)
except:
    pass

args = parser.parse_args()

# Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: {0}".format(args.log))
logging.basicConfig(level=numeric_level)

_LOGGER = logging.getLogger(__name__)


(READ_TABLE, WRITE_TABLE, READ_ZONES) = isystem_to_mqtt.tables.get_tables_translated(args.model, args.lang)


# Initialisation of mqtt client
base_topic = "heating/"

port_mqtt = 1883
client = mqtt.Client()
# client.on_log = on_log
if args.user:
    _LOGGER.debug("Authenticate with user %s", args.user)
    client.username_pw_set(args.user, args.password)
try:
    if args.tls:
        _LOGGER.debug("Set TLS mode.")
        client.tls_set(args.cacert, tls_version=args.tls)
        port_mqtt = 8883
except:
    pass

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
instrument = isystem_to_mqtt.isystem_modbus.ISystemInstrument(args.serial,
                                                              args.deviceid,
                                                              args.bimaster)
instrument.debug = False   # True or False


def read_zone(base_address, number_of_value):
    """ Read a MODBUS table zone and send the value to MQTT. """
    try:
        raw_values = instrument.read_registers(base_address, number_of_value)
    except EnvironmentError:
        logging.exception("I/O error")
    except ValueError:
        logging.exception("Value error")
    else:
        for index in range(0, number_of_value):
            address = base_address + index
            tag_definition = READ_TABLE.get(address)
            if tag_definition:
                tag_definition.publish(client, base_topic, raw_values, index)

def write_value(message):
    """ Write a value receive from MQTT to MODBUS """
    tag_definition = WRITE_TABLE.get(message.topic.strip(base_topic))
    if tag_definition:
        string_value = message.payload.decode("utf-8")
        value = tag_definition.convertion(string_value)
        _LOGGER.debug("write value %s : %s => address : %s = %s",
                      message.topic.strip(base_topic), string_value,
                      tag_definition.address, value)
        if value is not None:
            instrument.write_registers(tag_definition.address, value)


instrument.wait_time_slot()

# Main loop
while True:
    # update watchdog (reset by will)
    client.publish(base_topic + "reading", "ON", 1, True)
    # The total read time must be under the time slot duration
    start_time = time.time()
    for zone in READ_ZONES:
        if zone[1] == 0:
            instrument.wait_time_slot()
        else:
            read_zone(zone[0], zone[1])

    duration = time.time() - start_time
    _LOGGER.debug("Read take %1.3fs", duration)
    if duration > isystem_to_mqtt.isystem_modbus.MAXIMUM_OPERATION:
        _LOGGER.warning("Read take too long, wait_time_slot must be added between read_zone.")

    # Traitement de toute les ecritures ou attente de l'intervale
    try:
        waittime = args.interval
        while True:
            writeelement = write_queue.get(timeout=waittime)

            instrument.wait_time_slot()
            write_value(writeelement)
            waittime = 0
    except queue.Empty:
        # no more write, continue to read.
        instrument.wait_time_slot()
        continue

