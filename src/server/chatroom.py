import asyncio
import websockets
import random
from collections.abc import Iterable
from utils import logged
from user import User
from command_handler import CommandHandler

class Chatroom:
    """ 
    Chatroom manager for websocket based connections
    """
    
    def __init__(self):
        """ 
        Create a new chatroom
        """

        # Dict[Websocket, User]
        self.connected = dict()
        self.command_handler = CommandHandler()
    
    @logged
    async def handle_connection(self, websocket, name = None):
        """ 
        Registers a new websocket connection and notifies users

        Args:
            websocket (Websocket): new connection websocket
        """
        name = name if name is not None else self.generate_name()
        user = User(websocket, name)
        self.connected[websocket] = user
        await websocket.send(self.get_greeting(name))
        await self.send_to_all(self.get_connection_notification(name), websocket)

    @logged
    async def handle_message(self, websocket, message):
        """ 
        Handles incoming message:
            If it is a message, send to all users.
            If it is a command, process it

        Args:
            websocket (Websocket): websocket that sent message
            message (str): message sent
        """

        user = self.connected[websocket]
        if self.command_handler.is_command(message):
            await self.command_handler.handle_command(message, user, self)
            return

        outgoing_message = f"{user.name}: {message}"
        await self.send_to_all(outgoing_message)

    @logged
    async def handle_disconnect(self, websocket):
        """ 
        handles disconnect of websocket and notifies all connections

        Args:
            websocket (Websocket): Connection that was closed
        """
        user = self.connected.pop(websocket)
        await self.send_to_all(self.get_disconnect_notification(user.name))

    @logged
    async def send_to_all(self, message, skip = {}):
        """ 
        Send a message to all connected clients, except those in skip

        Args:
            message (str): message to send to all connections
            skip (set, optional): Websocket or Iterable[Websocket] to skip. Defaults to {}.
        """
        if not isinstance(skip, Iterable):
            skip = {skip}

        for conn in self.connected:
            if conn not in skip:
                await conn.send(message)

    @logged
    async def change_name(self, websocket, new_name):
        """
        Changes name of user connected with websocket to new_name

        Args:
            websocket (Websocket): connection to change name of
            new_name (str): new name for user
        """
        old_name = self.connected[websocket].name
        self.connected[websocket].name = new_name
        await self.send_to_all(f"\"{old_name}\" changed their name to \"{new_name}\"")

    def generate_name(self):
        """ 
        Generate a random client name str

        Returns:
            str: Randomly generated name
        """
        return f"Client {random.randint(1000, 9999)}"

    def get_greeting(self, name):
        """ 
        Generates greeting str for new connection

        Args:
            name (str): client name of new connection

        Returns:
            str: greeting for new connection
        """
        return f"Welcome, {name}! (hint: type \"!help\" for help)"

    def get_connection_notification(self, name):
        """ 
        Generates notification str for a new connection

        Args:
            name (str): name of new connection client

        Returns:
            str: notification for clients
        """
        return f"{name} has connected!"

    def get_disconnect_notification(self, name):
        """ 
        Generates disconnect notification str for disconnected client

        Args:
            name (str): name of disconnected client

        Returns:
            str: notification for clients
        """
        return f"{name} has disconnected!"


    def __str__(self):
        return f"Chatroom, connected: {self.connected}"
