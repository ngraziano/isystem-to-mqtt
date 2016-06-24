#!/usr/bin/env python
# -*- coding: utf8 -*-

import argparse
import ssl
import time
import minimalmodbus

import paho.mqtt.client as mqtt

class TagDefinition(object):
    """ Define a tag with mqtt topic and convertion """

    def __init__(self, tag_name, convertion, needed_value=1):
        self.tag_name = tag_name
        self.convertion = convertion
        self.needed_value = needed_value


def convert_tenth(raw_table, base_index):
    return raw_table[base_index] / 10

value_table = {
    601: TagDefinition("outside/temperature", convert_tenth),
    602: TagDefinition("boiler/temperature", convert_tenth),
    607: TagDefinition("boiler/return-temperature", convert_tenth),
    610: TagDefinition("boiler/pressure", convert_tenth),
    614: TagDefinition("zone-a/temperature", convert_tenth),
    615: TagDefinition("zone-a/calculated-temperature", convert_tenth),
    620: TagDefinition("boiler/calculated-temperature", convert_tenth)
    
}

parser = argparse.ArgumentParser() 
parser.add_argument("server", help="MQtt server to connect to.")
parser.add_argument("--user", help="MQtt username.")
parser.add_argument("--password", help="MQtt password.")
parser.add_argument("--interval", help="Check interval.", type=int, default=60)
parser.add_argument("--tls12", help="use TLS 1.2", dest="tls",
                    action="store_const", const=ssl.PROTOCOL_TLSv1_2)
parser.add_argument("--cacert", help="CA Certificate.",  default="/etc/ssl/certs/ca-certificates.crt")
parser.add_argument("--serial", help="Serial interface",  default="/dev/ttyUSB0")
parser.add_argument("--deviceid", help="Modbus device id", type=int,  default=10)
args = parser.parse_args()

# Initialisation of mqtt client

port_mqtt = 1883 
client = mqtt.Client()
# client.on_log = on_log
if args.user:
    client.username_pw_set(args.user,args.password)
if args.tls:
    client.tls_set(args.cacert,tls_version=args.tls)
    port_mqtt = 8883
client.connect(args.server, port_mqtt)
client.loop_start()

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

base_topic="heating/"

def read_zone(base_address, number_of_value):
    try:
        raw_values = instrument.read_registers(base_address, number_of_value)    
    except EnvironmentError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    else:
        for index in range(0, number_of_value):
            address = base_address + index
            tag_definition = value_table.get(address)
            if tag_definition:
                value = tag_definition.convertion(raw_values, index)
    #            print("value {}  = {}".format(tag_definition.tag_name, value))
                client.publish(base_topic + tag_definition.tag_name, value, retain=True)

while True:
    read_zone(600, 21)    
    time.sleep(args.interval)