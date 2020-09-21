import asyncio
import websockets
import random
from collections.abc import Iterable
from utils import logged

class Chatroom:

    
    def __init__(self):
        """ 
        Create a new chatroom
        """
        self.connected = dict()
    
    @logged
    async def handle_connection(self, websocket):
        """ Registers a new websocket connection and notifies users

        Args:
            websocket ([Websocket]): [new connection websocket]
        """
        name = self.generate_name()
        self.connected[websocket] = name
        await websocket.send(self.get_greeting(name))
        await self.send_to_all(self.get_connection_notification(name), websocket)

    @logged
    async def handle_message(self, websocket, message):
        """ Sends incoming message to all connections, including name

        Args:
            websocket ([Websocket]): [websocket that sent message]
            message ([str]): [message sent]
        """
        name = self.connected[websocket]
        outgoing_message = f"{name}: {message}"
        await self.send_to_all(outgoing_message)

    @logged
    async def handle_disconnect(self, websocket):
        """ handles disconnect of websocket and notifies all connections

        Args:
            websocket ([Websocket]): [Connection that was closed]
        """
        name = self.connected.get(websocket)
        self.connected.pop(websocket)
        await self.send_to_all(self.get_connection_notification(name))

    @logged
    async def send_to_all(self, message, skip = {}):
        """ Send a message to all connected clients, except those in skip

        Args:
            message ([str]): [message to send to all connections]
            skip (set, optional): [Websocket or Iterable[Websocket] to skip]. Defaults to {}.
        """
        if not isinstance(skip, Iterable):
            skip = {skip}

        for conn in self.connected:
            if conn not in skip:
                await conn.send(message)

    def generate_name(self):
        """ Generate a random client name str

        Returns:
            [str]: [Randomly generated name]
        """
        return f"Client {random.randint(1000, 9999)}"

    def get_greeting(self, name):
        """ Generates greeting str for new connection

        Args:
            name ([str]): [client name of new connection]

        Returns:
            [str]: [greeting for new connection]
        """
        return f"Welcome, {name}!"

    def get_connection_notification(self, name):
        """ Generates notification str for a new connection

        Args:
            name ([str]): [name of new connection client]

        Returns:
            [str]: [notification for clients]
        """
        return f"{name} has connected!"

    def get_disconnect_notification(self, name):
        """ Generates disconnect notification str for disconnected client

        Args:
            name ([str]): [name of disconnected client]

        Returns:
            [str]: [notification for clients]
        """
        return f"{name} has disconnected!"
