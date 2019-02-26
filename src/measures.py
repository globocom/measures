import socket
import json
import time
import logging
import functools


logger = logging.getLogger(__name__)


class _TimeContext(object):

    def __init__(self, socket, client, address, metric):
        self.socket = socket
        self.client = client
        self.address = address
        self.metric = metric
        self.dimensions = {}

    def __enter__(self):
        self.start_time = time.time()
        return self.dimensions

    def __exit__(self, exc_type, exc_value, exc_traceback):
        spent = time.time() - self.start_time
        message = {
            'client': self.client,
            'metric': self.metric,
            'time': spent,
            'error_type': str(exc_type or ''),
            'error_value': str(exc_value or ''),
        }
        self.dimensions.update(message)
        send_to(self.socket, self.address, self.dimensions)


class Measure(object):

    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)
        self.time = functools.partial(_TimeContext, self.socket, client, address)

    def count(self, metric, counter=1, dimensions=None):
        message = {
            'client': self.client,
            'metric': metric,
            'count': counter,
        }
        dimensions = dimensions or {}
        dimensions.update(message)
        send_to(self.socket, self.address, dimensions)

    def send(self, metric, dimensions):
        message = {
            'metric': metric,
            'client': self.client,
        }
        dimensions = dimensions or {}
        dimensions.update(message)
        send_to(self.socket, self.address, dimensions)


def send_to(socket_obj, address, dimensions):
    buf = json.dumps(dimensions).encode('utf-8')
    try:
        socket_obj.sendto(buf, address)
    except socket.error as serr:
        logger.error('Error on sendto. [Errno {} - {}]'.format(serr.errno, serr.strerror))

