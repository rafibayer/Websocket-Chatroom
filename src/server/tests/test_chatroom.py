import unittest
import asyncio
import os
import sys
import test_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc
from chatroom import Chatroom
from response import Response, Origin


class TestServer(unittest.TestCase):

    def test_create_chatroom(self):
        room = Chatroom("../config/test_config/chat.yaml")
        self.assertIsNotNone(room.connected)

    def test_handle_connection(self):
        room = Chatroom("../config/test_config/chat.yaml")
        fake_websocket = Mwsc()
        self.connect_fake_client(fake_websocket, room)

        self.assertIn(fake_websocket, room.connected)
        self.assertEqual(room.connected[fake_websocket].websocket, fake_websocket)
        self.assertTrue(len(room.connected[fake_websocket].websocket.incoming) > 0)
        self.assertEqual(len(room.connected), 1)

    def test_handle_message(self):
        room = Chatroom("../config/test_config/chat.yaml")
        fake_websocket = Mwsc()
        fake_websocket2 = Mwsc()
        self.connect_fake_client(fake_websocket, room)
        self.connect_fake_client(fake_websocket2, room)
        asyncio.get_event_loop().run_until_complete(room.handle_message(fake_websocket, "Fake message"))

        self.assertIn(fake_websocket, room.connected)
        self.assertEqual(room.connected[fake_websocket].websocket, fake_websocket)
        self.assertTrue(len(room.connected[fake_websocket2].websocket.incoming) > 1)

    def test_handle_disconnect(self):
        room = Chatroom("../config/test_config/chat.yaml")
        fake_websocket = Mwsc()
        self.assertEqual(len(room.connected), 0)
        self.connect_fake_client(fake_websocket, room)
        self.assertEqual(len(room.connected), 1)
        asyncio.get_event_loop().run_until_complete(room.handle_disconnect(fake_websocket))
        self.assertEqual(len(room.connected), 0)

    def test_send_to_all(self):
        room = Chatroom("../config/test_config/chat.yaml")
        fake_websocket = Mwsc()
        fake_websocket2 = Mwsc()

        self.connect_fake_client(fake_websocket, room)
        self.connect_fake_client(fake_websocket2, room)
        resp = Response("TO ALL")
        asyncio.get_event_loop().run_until_complete(room.send_to_all(resp, fake_websocket2))

        self.assertEqual(resp.json(), room.connected[fake_websocket].websocket.incoming[-1])
        self.assertNotEqual(resp.json(), room.connected[fake_websocket2].websocket.incoming[-1])

    def test_name_change(self):
        room = Chatroom("../config/test_config/chat.yaml")
        fake_websocket = Mwsc()
        fake_websocket2 = Mwsc()
        self.connect_fake_client(fake_websocket, room, "old_name")
        self.connect_fake_client(fake_websocket2, room)
        asyncio.get_event_loop().run_until_complete(room.change_name(fake_websocket, "new_name"))

        expected = Response(room.get_name_change_notification("old_name", "new_name"), Origin.SERVER)

        self.assertEqual(expected.json(), room.connected[fake_websocket].websocket.incoming[-1])
        self.assertEqual(expected.json(), room.connected[fake_websocket2].websocket.incoming[-1])
        self.assertEqual(room.connected[fake_websocket].name, "new_name")

    def test_handle_shutdown(self):
        room = Chatroom("../config/test_config/chat.yaml")
        fake_websocket = Mwsc()
        fake_websocket2 = Mwsc()
        self.connect_fake_client(fake_websocket, room)
        self.connect_fake_client(fake_websocket2, room)

        asyncio.get_event_loop().run_until_complete(room.handle_shutdown())

        expected = Response(room.get_shutdown_notification(), Origin.SERVER)

        self.assertIn(str(expected), str(room.connected[fake_websocket].websocket.incoming[-1]))
        self.assertIn(str(expected), str(room.connected[fake_websocket2].websocket.incoming[-1]))
        self.assertFalse(room.connected[fake_websocket].websocket.open)
        self.assertFalse(room.connected[fake_websocket2].websocket.open)

    def connect_fake_client(self, fake_websocket, chatroom, name=None):
        asyncio.get_event_loop().run_until_complete(chatroom.handle_connection(fake_websocket, name))


if __name__ == '__main__':
    unittest.main()
