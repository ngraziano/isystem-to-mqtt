""" Unit test for TagDefinition class """

import unittest.mock as mock
import unittest

import paho.mqtt.client as mqtt

from .. import convert
from .. import tag_definition


class TestTagDefinion(unittest.TestCase):
    """ Test for MultipleTagDefinition """
    def test_simple_puplish(self):
        """ Test a simple call """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.TagDefinition("test/test1", convert.unit)

        tag.publish(client, "base/", [1], 0)

        client.publish.assert_called_once_with("base/test/test1", 1, retain=True)
    def test_multiple_same_puplish(self):
        """ Test a simple call """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.TagDefinition("test/test1", convert.unit)

        tag.publish(client, "base/", [1], 0)
        tag.publish(client, "base/", [1], 0)

        client.publish.assert_called_once_with("base/test/test1", 1, retain=True)

    def test_multiple_puplish(self):
        """ Test a simple call """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.TagDefinition("test/test1", convert.unit)

        tag.publish(client, "base/", [1], 0)
        tag.publish(client, "base/", [1], 0)
        tag.publish(client, "base/", [2], 0)

        calls = [mock.call("base/test/test1", 1, retain=True),
                 mock.call("base/test/test1", 2, retain=True)]
        client.publish.assert_has_calls(calls)
