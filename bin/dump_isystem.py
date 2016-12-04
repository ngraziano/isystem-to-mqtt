#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import logging

import isystem_to_mqtt.isystem_dumper

def main():
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

    dumper = isystem_to_mqtt.isystem_dumper.ISystemDumper(args)

    dumper.dump_system(args.start, args.number)

if __name__ == '__main__':
    main()
