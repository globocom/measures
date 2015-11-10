from ..acceptance import UDPServerTestCase
from measures import Measure
from multiprocessing import Process
import json
import time


class MeasureTestCase(UDPServerTestCase):

    def setUp(self):
        super(MeasureTestCase, self).setUp()
        self.measure = Measure('myclient', ('127.0.0.1', 1984))

    def test_recieve_count_message_correctly_over_network(self):
        self.measure.count('mymetric')
        self.wait_for(lambda: len(self.messages))
        self.assertEqual(len(self.messages), 1)

        message = json.loads(self.messages[0].decode('utf-8'))
        expected_message = {
            'client': 'myclient',
            'metric': 'mymetric',
            'count': 1,
        }
        self.assertDictEqual(message, expected_message)

    def test_recieve_time_message_correctly_over_network(self):
        with self.measure.time('mymetric'):
            pass

        while True:
            self.wait_for(lambda: len(self.messages))
            message = json.loads(self.messages.pop().decode('utf-8'))

            if 'time' in message:
                break

        self.assertIsInstance(message['time'], float)
        self.assertIn('client', message)
        self.assertEqual(message['client'], 'myclient')
        self.assertIn('metric', message)
        self.assertEqual(message['metric'], 'mymetric')
        self.assertGreater(message['time'], 0)
        self.assertIn('error_type', message)
        self.assertEqual(message['error_type'], '')
        self.assertIn('error_value', message)
        self.assertEqual(message['error_value'], '')

    def test_count_must_not_hang_if_server_is_up(self):
        p = Process(target=lambda: self.measure.count('mymetric'))
        p.start()
        p.join(0.3)
        self.assertFalse(p.is_alive())
        p.terminate()

    def test_time_must_not_hang_if_server_is_up(self):
        p = Process(target=lambda: self.measure.time('mymetric'))
        p.start()
        p.join(0.3)
        self.assertFalse(p.is_alive())
        p.terminate()

    def test_count_must_not_hang_if_server_is_down(self):
        self.__class__.stop_server()
        time.sleep(0.5)
        p = Process(target=lambda: self.measure.count('mymetric'))
        p.start()
        p.join(0.3)
        self.assertFalse(p.is_alive())
        p.terminate()

    def test_time_must_not_hang_if_server_is_down(self):
        self.__class__.stop_server()
        time.sleep(0.5)
        p = Process(target=lambda: self.measure.time('mymetric'))
        p.start()
        p.join(0.3)
        self.assertFalse(p.is_alive())
        p.terminate()
