#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='isystem-to-mqtt',
    version='0.1.0',
    author='Mickael Le Baillif',
    author_email='nicolas.graziano+py@gmail.com',
    # packages=['isystem-tom-qtt'],
    scripts=['bin/poll_isystem_mqtt.py'],
    url='https://github.com/ngraziano/isystem-to-mqtt',
    install_requires=['MinimalModbus', 'paho-mqtt'],
    # license='LICENSE.txt',
    description='Request Isystem boiler and send value to mqtt',
    # long_description=open('README.md').read(),
)
