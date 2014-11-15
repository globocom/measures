# -*- coding: utf8 -*-

from unittest import TestCase
from measure import Measure
from mock import patch
import json
import socket


class MeasureTestCase(TestCase):

    def setUp(self):
        self.measure = Measure('myclient', ('localhost', 1984))

    def test_must_create_a_measure_object_with_correct_attributes(self):
        measure = Measure('myclient', ('localhost', 1984))
        self.assertEqual(measure.client, 'myclient')
        self.assertEqual(measure.address, ('localhost', 1984))
        self.assertEqual(measure.socket.type, socket.SOCK_DGRAM)

    @patch('socket.socket.sendto')
    def test_must_send_a_packet_to_correct_address(self, mock_sendto):
        self.measure.count('mymetric')
        self.assertEqual(mock_sendto.call_count, 1)
        self.assertEqual(mock_sendto.call_args[0][1], ('localhost', 1984))

    @patch('socket.socket.sendto')
    def test_must_send_a_packet_with_counter_of_one(self, mock_sendto):
        self.measure.count('mymetric')

        self.assertEqual(mock_sendto.call_count, 1)

        expected_message = {'client': 'myclient', 'metric': 'mymetric', 'count': 1}
        message = json.loads(mock_sendto.call_args[0][0])
        self.assertDictEqual(message, expected_message)

    @patch('socket.socket.sendto')
    def test_must_send_a_packet_with_metric_counter_of_ten(self, mock_sendto):
        self.measure.count('mymetric', counter=10)

        self.assertEqual(mock_sendto.call_count, 1)

        expected_message = {'client': 'myclient', 'metric': 'mymetric', 'count': 10}
        message = json.loads(mock_sendto.call_args[0][0])
        self.assertDictEqual(message, expected_message)

    @patch('socket.socket.sendto')
    def test_must_send_packet_with_dimensions(self, mock_sendto):
        self.measure.count('mymetric', dimensions={'name': 'john'})

        self.assertEqual(mock_sendto.call_count, 1)
        expected_message = {
            'client': 'myclient',
            'metric': 'mymetric',
            'count': 1,
            'name': 'john',
        }
        message = json.loads(mock_sendto.call_args[0][0])
        self.assertDictEqual(message, expected_message)

    @patch('socket.socket.sendto')
    def test_dimensions_must_not_override_parameters(self, mock_sendto):
        self.measure.count('mymetric', dimensions={'client': 'otherclient', 'metric': 'othermetric', 'count': 10})

        self.assertEqual(mock_sendto.call_count, 1)
        expected_message = {
            'client': 'myclient',
            'metric': 'mymetric',
            'count': 1,
        }
        message = json.loads(mock_sendto.call_args[0][0])
        self.assertDictEqual(message, expected_message)

    @patch('socket.socket.sendto')
    def test_must_not_change_dimensions_dict(self, mock_sendto):
        dimensions = {}
        self.measure.count('mymetric', dimensions=dimensions)
        self.assertFalse(dimensions)
