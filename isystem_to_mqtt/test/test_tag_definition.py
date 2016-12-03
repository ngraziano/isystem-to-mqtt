""" Unit test for TagDefinition class """
try:
    import unittest.mock as mock
except ImportError:
    import mock

import unittest

import paho.mqtt.client as mqtt

from .. import convert
from .. import tag_definition


class TestTagDefinion(unittest.TestCase):
    """ Test for TagDefinition """

    def test_simple_puplish(self):
        """ Test a simple call """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.TagDefinition("test/test1", convert.unit)

        tag.publish(client, "base/", [1], 0)

        client.publish.assert_called_once_with(
            "base/test/test1", 1, retain=True)

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
        self.assertEqual(2, client.publish.call_count)


class TestMultipleTagDefinition(unittest.TestCase):
    """ Test for MultipleTagDefinition """
    def test_simple_publish(self):
        """ MultipleTagDefinition Test a simple call """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.MultipleTagDefinition(
            [("test/test1", convert.unit),
             ("test/test2", convert.unit)])

        tag.publish(client, "base/", [1], 0)

        calls = [mock.call("base/test/test1", 1, retain=True),
                 mock.call("base/test/test2", 1, retain=True)]
        client.publish.assert_has_calls(calls)
        self.assertEqual(2, client.publish.call_count)

    def test_multiple_same_puplish(self):
        """ MultipleTagDefinition Test multiple call with same value """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.MultipleTagDefinition(
            [("test/test1", convert.unit),
             ("test/test2", convert.unit)])

        tag.publish(client, "base/", [1], 0)
        tag.publish(client, "base/", [1], 0)

        calls = [mock.call("base/test/test1", 1, retain=True),
                 mock.call("base/test/test2", 1, retain=True)]
        client.publish.assert_has_calls(calls)
        self.assertEqual(2, client.publish.call_count)

    def test_multiple_puplish(self):
        """ MultipleTagDefinition Test multiple call with different value """
        client = mock.MagicMock(spec=mqtt.Client)
        tag = tag_definition.MultipleTagDefinition(
            [("test/test1", convert.unit),
             ("test/test2", convert.unit)])

        tag.publish(client, "base/", [1], 0)
        tag.publish(client, "base/", [1], 0)
        tag.publish(client, "base/", [2], 0)

        calls = [mock.call("base/test/test1", 1, retain=True),
                 mock.call("base/test/test2", 1, retain=True),
                 mock.call("base/test/test1", 2, retain=True),
                 mock.call("base/test/test2", 2, retain=True)]
        client.publish.assert_has_calls(calls)
        self.assertEqual(4, client.publish.call_count)
