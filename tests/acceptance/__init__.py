try:
    from SocketServer import ThreadingMixIn, UDPServer
except ImportError:
    # PY3
    from socketserver import ThreadingMixIn, UDPServer

from unittest import TestCase
from threading import Thread
from contextlib import contextmanager
import socket
import time


class ServerRunningError(Exception):
    pass


class ServerNotRunningError(Exception):
    pass


class ThreadedUDPServer(ThreadingMixIn, UDPServer):
    pass


class UDPServerTestCase(TestCase):

    port = 1984
    server_running = False

    @classmethod
    def _message_handler(cls, message, addr, server):
        cls.messages.append(message[0])

    @classmethod
    def tearDownClass(cls):
        cls.stop_server()

    @classmethod
    def start_server(cls):
        if cls.server_running:
            raise ServerRunningError()
        cls.messages = []
        final_time = time.time() + 5
        while True:
            try:
                cls.server = ThreadedUDPServer(('127.0.0.1', cls.port), cls._message_handler)
            except socket.error as serr:
                # address already in use
                if serr.errno == 48 and time.time() < final_time:
                    continue
            break
        cls.thread = Thread(target=cls.server.serve_forever)
        cls.thread.start()
        cls.server_running = True

    @classmethod
    def stop_server(cls):
        if not cls.server_running:
            raise ServerNotRunningError()
        cls.server.shutdown()
        cls.thread.join()
        cls.server_running = False

    def setUp(self):
        super(UDPServerTestCase, self).setUp()
        self.__class__.messages = []
        if not self.__class__.server_running:
            self.__class__.start_server()

    def wait_for(self, condition, timeout=5):
        final_time = time.time() + timeout
        while not condition() and time.time() < final_time:
            pass
