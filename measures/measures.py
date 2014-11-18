import socket
import json
import time
import logging


logger = logging.getLogger(__name__)


class Measure(object):

    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)

    def count(self, metric, counter=1, dimensions={}):
        message = {
            'client': self.client,
            'metric': metric,
            'count': counter,
        }
        message = dict(dimensions.items() + message.items())
        try:
            self.socket.sendto(json.dumps(message), self.address)
        except socket.error as serr:
            logger.error('Error on sendto. [Errno {}]'.format(serr.errno))
