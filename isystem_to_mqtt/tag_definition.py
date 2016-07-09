import logging

_LOGGER = logging.getLogger(__name__)


class TagDefinition(object):
    """ Define a tag with mqtt topic and convertion """

    def __init__(self, tag_name, convertion, needed_value=1):
        self.tag_name = tag_name
        self.convertion = convertion
        self.needed_value = needed_value

    def publish(self, client, base_topic, raw_values, index):
        """ Publish the converted value to mqtt using client parameter"""
        value = self.convertion(raw_values, index)
        _LOGGER.debug("value %s  = %s", self.tag_name, value)
        client.publish(base_topic + self.tag_name, value, retain=True)

class MultipleTagDefinition(object):
    """ Define a tag with multiple mqtt topic and convertion """

    def __init__(self, definition_list, needed_value=1):
        self.definition_list = definition_list
        self.needed_value = needed_value

    def publish(self, client, base_topic, raw_values, index):
        """ Publish the converted value to mqtt using client parameter"""
        for (convertion,tag_name) in self.definition_list:
            value = convertion(raw_values, index)
            _LOGGER.debug("value %s  = %s", tag_name, value)
            client.publish(base_topic + tag_name, value, retain=True)


class WriteTagDefinition(object):
    """ Define a tag to write with address and convertion """

    def __init__(self, address, convertion):
        self.address = address
        self.convertion = convertion
