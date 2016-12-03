#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='isystem-to-mqtt',
    version='0.2.0',
    author='Nicolas Graziano',
    author_email='nicolas.graziano+py@gmail.com',
    packages= find_packages(),
    scripts=['bin/poll_isystem_mqtt.py', 'bin/dump_isystem.py'],
    url='https://github.com/ngraziano/isystem-to-mqtt',
    install_requires=['MinimalModbus', 'paho-mqtt'],
    license='LICENSE',
    description='Request Isystem boiler and send value to mqtt',
    classifiers=['Programming Language :: Python :: 3']
    # long_description=open('README.md').read(),
)
