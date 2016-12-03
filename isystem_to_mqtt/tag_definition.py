from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging


_LOGGER = logging.getLogger(__name__)


class TagDefinition(object):
    """ Define a tag with mqtt topic and convertion """

    def __init__(self, tag_name, convertion, needed_value=1):
        self.tag_name = tag_name
        self.convertion = convertion
        self.needed_value = needed_value
        self.last_value = None

    def publish(self, client, base_topic, raw_values, index):
        """ Publish the converted value to mqtt using client parameter"""
        value = self.convertion(raw_values, index)
        _LOGGER.debug("value %s  = %s", self.tag_name, value)
        if value != self.last_value:
            client.publish(base_topic + self.tag_name, value, retain=True)
            self.last_value = value

    def print(self, raw_values, index):
        """ Print the converted value """
        value = self.convertion(raw_values, index)
        print("\t{0}\t{1}".format(self.tag_name, value), end='')

class MultipleTagDefinition(object):
    """ Define a tag with multiple mqtt topic and convertion """

    def __init__(self, definition_list, needed_value=1):
        self.definition_list = definition_list
        self.needed_value = needed_value
        self.last_value = [None] * len(definition_list)

    def publish(self, client, base_topic, raw_values, index):
        """ Publish the converted value to mqtt using client parameter"""
        i = 0
        for (tag_name, convertion) in self.definition_list:
            value = convertion(raw_values, index)
            _LOGGER.debug("value %s  = %s", tag_name, value)
            if value != self.last_value[i]:
                client.publish(base_topic + tag_name, value, retain=True)
                self.last_value[i] = value
            i += 1

    def print(self, raw_values, index):
        """ Print the converted value """
        for (tag_name, convertion) in self.definition_list:
            value = convertion(raw_values, index)
            print("\t{0}\t{1}".format(tag_name, value), end='')


class WriteTagDefinition(object):
    """ Define a tag to write with address and convertion """

    def __init__(self, address, convertion):
        self.address = address
        self.convertion = convertion
