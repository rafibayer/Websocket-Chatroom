import unittest
import asyncio
import os
import sys
import test_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from chatroom import Chatroom
from command_handler import CommandHandler
from user import User
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc
from response import Response, Origin


class TestCommandHandler(unittest.TestCase):

    def test_help_registered(self):
        handler = CommandHandler()
        self.assertIn("!help", handler.registered_commands)

    def test_is_command(self):
        handler = CommandHandler()

        valid = ["!valid", "!help", "!valid with args"]
        invalid = ["message", "message 2", "message!", "!", "message !three"]

        for s in valid:
            self.assertTrue(handler.is_command(s))

        for s in invalid:
            self.assertFalse(handler.is_command(s))

    def test_help(self):
        handler = CommandHandler()
        room = Chatroom("../config/test_config/chat.yaml")
        socket = Mwsc()
        user = User(socket, "Test")
        test_helper.sync(handler.handle_command("!help", user, room))
        self.assertTrue("!help" in user.websocket.incoming[-1])

    def test_bad_command(self):
        handler = CommandHandler()
        room = Chatroom("../config/test_config/chat.yaml")
        socket = Mwsc()
        user = User(socket, "Test")

        test_helper.sync(handler.handle_command("!fake", user, room))
        self.assertTrue("not a valid" in user.websocket.incoming[-1])

    def test_pm(self):
        room = Chatroom("../config/test_config/chat.yaml")
        sender = Mwsc()
        reciever = Mwsc()
        bystander = Mwsc()

        test_helper.sync(room.handle_connection(sender, "sender"))
        test_helper.sync(room.handle_connection(reciever, "reciever"))
        test_helper.sync(room.handle_connection(bystander, "bystander"))

        test_helper.sync(
            room.command_handler.handle_command("!pm reciever MESSAGE BODY", room.connected[sender], room)
        )

        expected_reciver = room.get_outgoing_pm("MESSAGE BODY", "sender")
        expected_sender = room.get_pm_receipt("MESSAGE BODY", "reciever")

        self.assertIn(expected_reciver, reciever.incoming[-1])
        self.assertIn("PRIVATE", reciever.incoming[-1])

        self.assertIn(expected_sender, sender.incoming[-1])
        self.assertIn("PRIVATE", sender.incoming[-1])

        self.assertNotIn(expected_sender, bystander.incoming[-1])
        self.assertNotIn("PRIVATE", bystander.incoming[-1])

    def test_bad_pm(self):

        room = Chatroom("../config/test_config/chat.yaml")
        sender = Mwsc()
        reciever = Mwsc()

        test_helper.sync(room.handle_connection(sender, "sender"))
        test_helper.sync(room.handle_connection(reciever, "reciever"))

        test_helper.sync(
            room.command_handler.handle_command("!pm", room.connected[sender], room)
        )

        test_helper.sync(
            room.command_handler.handle_command("!pm test", room.connected[sender], room)
        )

        test_helper.sync(
            room.command_handler.handle_command("!pm test ", room.connected[sender], room)
        )


if __name__ == '__main__':
    unittest.main()
