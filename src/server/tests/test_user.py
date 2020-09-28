import unittest
import asyncio
import os
import sys
import test_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc
from user import User


class TestUser(unittest.TestCase):

    def test_create_user(self):
        name = "Rafi"

        fake_socket = Mwsc()
        user = User(fake_socket, name)
        self.assertIsNotNone(user.websocket)
        self.assertIsNotNone(user.name)
        self.assertIsNotNone(user.connected_at)
        self.assertEqual(user.name, name)


if __name__ == '__main__':
    unittest.main()
