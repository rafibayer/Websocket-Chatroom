import unittest
import asyncio
import threading
import time
from server import Server
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc

class TestServer(unittest.TestCase):

    def test_create_server(self):
        host = "localhost"
        port = 5000

        server = Server(host, port)

        self.assertEqual(server.port, port)
        self.assertEqual(server.host, host)
        self.assertFalse(server.running)
        self.assertIsNotNone(server.chatroom)

    ## yikes
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