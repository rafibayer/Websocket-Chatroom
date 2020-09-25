import asyncio
import websockets
import random
from string import Template
from collections.abc import Iterable
from utils import logged
from user import User
from command_handler import CommandHandler
from config_manager import ConfigManager

class Chatroom:
    """ 
    Chatroom manager for websocket based connections
    """
    
    def __init__(self, chat_config_path):
        """
        Create a new Chatroom

        Args:
            chat_config_path (str): path to chat config yaml
        """

        # Dict[Websocket, User]
        self.connected = dict()
        self.command_handler = CommandHandler()
        self.config = ConfigManager(chat_config_path)
        self.name_generator = AdjAnimalNameGenerator(
            self.config["name_generator"]["adjective_path"],
            self.config["name_generator"]["animal_path"])
    
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
        await self.send_to_all(outgoing_message, websocket)

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
    async def handle_shutdown(self):
        """
        Notifies all clients of shutdown and closes their connections
        """
        await self.send_to_all(self.get_shutdown_notification())
        for conn in self.connected.keys():
            print(f"closing {conn}")
            await conn.close()

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
        await self.send_to_all(self.get_name_change_notification(old_name, new_name))

    def generate_name(self):
        """ 
        Generate an initial name for a new client

        Returns:
            str: Randomly generated name
        """
       
        return self.name_generator.generate_name()

    def get_greeting(self, name):
        """ 
        Generates greeting str for new connection

        Args:
            name (str): client name of new connection

        Returns:
            str: greeting for new connection
        """
        return Template(self.config["greeting_temp"]).substitute(name=name)

    def get_connection_notification(self, name):
        """ 
        Generates notification str for a new connection

        Args:
            name (str): name of new connection client

        Returns:
            str: notification for clients
        """
        return Template(self.config["conn_notif_temp"]).substitute(name=name)

    def get_disconnect_notification(self, name):
        """ 
        Generates disconnect notification str for disconnected client

        Args:
            name (str): name of disconnected client

        Returns:
            str: notification for clients
        """
        return Template(self.config["disconn_notif_temp"]).substitute(name=name)

    def get_name_change_notification(self, old_name, new_name):
        """
        Generates name change notification

        Args:
            old_name (str): old name, before change
            new_name (str): new name, after change

        Returns:
            str: notification for clients
        """
        return Template(self.config["namechange_notif_temp"]).substitute(old=old_name, new=new_name)

    def get_shutdown_notification(self):
        """
        Generates server shutdown notification

        Returns:
            str: notification for clients
        """
        return self.config["shutdown_notif_temp"]


    def __str__(self):
        return f"Chatroom, connected: {self.connected}"

class AdjAnimalNameGenerator:

    def __init__(self, adj_path, animal_path):
        with open(adj_path) as adjs:
            self.adjectives = [l.strip().capitalize() for l in adjs.readlines()]
        with open(animal_path) as animals:
            self.animals = [l.strip().capitalize() for l in animals.readlines()]

    def generate_name(self):
        return f"{random.choice(self.adjectives)}{random.choice(self.animals)}"