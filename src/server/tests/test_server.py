import unittest
import asyncio
import threading
import time
import os
import sys
import test_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from server import Server
from chatroom import Chatroom
from config_manager import ConfigManager
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc


class TestServer(unittest.TestCase):

    def test_create_server(self):

        server_config = ConfigManager("../config/test_config/server.yaml")
        chat = Chatroom("../config/test_config/chat.yaml")
        server = Server("../config/test_config/server.yaml", chat)

        self.assertEqual(server.port, server_config["port"])
        self.assertEqual(server.host, server_config["host"])
        self.assertFalse(server.running)
        self.assertIsNotNone(server.handler)
        self.assertEqual(server.handler, chat)

    # yikes
    # def test_server_start(self):
    #     startup_delay = 3.0
    #     host = "localhost"
    #     port = 5000

    #     server = Server(host, port)
    #     loop = asyncio.new_event_loop()

    #     def otherthread():
    #         print(id(server))
    #         asyncio.set_event_loop(loop)
    #         server.start()

    #     thread = threading.Thread(target=otherthread)
    #     thread.start()
    #     time.sleep(startup_delay)
    #     self.assertTrue(server.running)
    #     server.stop()
    #     thread.join()


if __name__ == '__main__':
    unittest.main()
