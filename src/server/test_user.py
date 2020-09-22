import unittest
import asyncio
from user import User
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc

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