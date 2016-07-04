#!/usr/bin/env python
# -*- coding: utf8 -*-

import argparse
import ssl
import queue
import minimalmodbus

import paho.mqtt.client as mqtt

from isystem_to_mqtt.tables import READ_TABLE, WRITE_TABLE

parser = argparse.ArgumentParser()
parser.add_argument("server", help="MQtt server to connect to.")
parser.add_argument("--user", help="MQtt username.")
parser.add_argument("--password", help="MQtt password.")
parser.add_argument("--interval", help="Check interval.", type=int, default=60)
parser.add_argument("--tls12", help="use TLS 1.2", dest="tls",
                    action="store_const", const=ssl.PROTOCOL_TLSv1_2)
parser.add_argument("--cacert", help="CA Certificate.", default="/etc/ssl/certs/ca-certificates.crt")
parser.add_argument("--serial", help="Serial interface", default="/dev/ttyUSB0")
parser.add_argument("--deviceid", help="Modbus device id", type=int, default=10)
args = parser.parse_args()

# Initialisation of mqtt client

base_topic="heating/"

port_mqtt = 1883 
client = mqtt.Client()
# client.on_log = on_log
if args.user:
    client.username_pw_set(args.user,args.password)
if args.tls:
    client.tls_set(args.cacert,tls_version=args.tls)
    port_mqtt = 8883

client.will_set(base_topic + "reading", "OFF", 1, True)

write_queue = queue.Queue()

def on_message(the_client, userdata, message):
    write_queue.put(message)

client.on_message = on_message

subscribe_list = [(base_topic + name, 0) for name in WRITE_TABLE.keys()]

def on_connect(the_client, userdata, flags, rc):
    if (rc==mqtt.CONNACK_ACCEPTED):
        the_client.subscribe(subscribe_list)

client.on_connect = on_connect

client.connect(args.server, port_mqtt)
client.loop_start()

client.publish(base_topic + "reading", "ON", 1, True)


# Initialisation of Modbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
instrument = minimalmodbus.Instrument(args.serial, args.deviceid)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
# seconds (0.05 par defaut)
instrument.serial.timeout = 1
instrument.debug = False   # True or False
instrument.mode = minimalmodbus.MODE_RTU

def read_zone(base_address, number_of_value):
    try:
        raw_values = instrument.read_registers(base_address, number_of_value)
    except EnvironmentError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    else:
        for index in range(0, number_of_value):
            address = base_address + index
            tag_definition = READ_TABLE.get(address)
            if tag_definition:
                value = tag_definition.convertion(raw_values, index)
                print("value {}  = {}".format(tag_definition.tag_name, value))
                client.publish(base_topic + tag_definition.tag_name, value, retain=True)

def write_value(message):
    tag_definition = WRITE_TABLE.get(message.topic.strip(base_topic))
    if tag_definition:
        value = tag_definition.convertion(message.payload)
        print("write value {} : add : {} = {}".format(message.topic.strip(base_topic), tag_definition.address ,value))
        instrument.write_registers(tag_definition.address,value)

# Main loop
while True:
    read_zone(600, 21)
    read_zone(507, 4)
    read_zone(650, 10)
    read_zone(231, 1)
    # Traitement de toute les ecritures
    try:
        waittime = args.interval
        while True:
            writeelement = write_queue.get(timeout=waittime)
            write_value(writeelement)
            waittime = 0
    except queue.Empty:
        continue

