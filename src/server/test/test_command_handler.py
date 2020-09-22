import unittest
import asyncio
from context import Chatroom, CommandHandler, User
from mock.mockwebsocketclient import MockWebsocketClient as Mwsc

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
        socket = Mwsc()
        user = User(socket, "Test")
        asyncio.get_event_loop().run_until_complete(handler.handle_command("!help", user, None))
        self.assertTrue("!help" in user.websocket.incoming[-1])

    def test_bad_command(self):
        handler = CommandHandler()
        socket = Mwsc()
        user = User(socket, "Test")

        asyncio.get_event_loop().run_until_complete(handler.handle_command("!fake", user, None))
        self.assertTrue("not a valid" in user.websocket.incoming[-1])


if __name__ == '__main__':
    unittest.main()