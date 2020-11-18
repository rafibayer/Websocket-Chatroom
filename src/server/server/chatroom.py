"""
Chatroom defines handlers for client behavior such as connecting and sending messages
"""
import random
import logging
from string import Template
from collections.abc import Iterable
from utils import log, log_message
from user import User
from command_handler import CommandHandler
from config_manager import ConfigManager
from response import Response, Origin

logger = logging.getLogger(__name__)


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
        self.env = self.config["meta"]["enviornment"]

    @log(logger, logging.INFO)
    async def handle_connection(self, websocket, name=None):
        """
        Registers a new websocket connection and notifies users

        Args:
            websocket (Websocket): new connection websocket
        """
        name = name if name is not None else self.generate_name()
        user = User(websocket, name)
        self.connected[websocket] = user
        await self.send(Response(self.get_greeting(name), Origin.SERVER), websocket)
        await self.send_to_all(Response(self.get_connection_notification(name), Origin.SERVER), websocket)

    @log(logger, logging.INFO)
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

        body = f"{user.name}: {message}"
        all_response = Response(body, Origin.USER)
        sender_response = Response(body, Origin.SELF)
        await self.send_to_all(all_response, websocket)
        await self.send(sender_response, websocket)

    @log(logger, logging.INFO)
    async def handle_disconnect(self, websocket):
        """
        handles disconnect of websocket and notifies all connections

        Args:
            websocket (Websocket): Connection that was closed
        """
        user = self.connected.pop(websocket)
        await self.send_to_all(Response(self.get_disconnect_notification(user.name), Origin.SERVER))

    @log(logger, logging.INFO)
    async def send(self, response, websocket):
        """Send a response to a websocket

        Args:
            response (Response): The Response to send
            websocket (Websocket): The websocket to send the Response to
        """
        if not isinstance(response, Response):
            log_message(f"Outgoing: {response} is not of type Response, preventing send", logging.CRITICAL)
            return

        if response.data["origin"] == Origin.DEFAULT:
            log_message(f"Outgoing response has DEFAULT origin", logging.WARNING)

        await websocket.send(response.json())

    @log(logger, logging.INFO)
    async def send_to_all(self, response, skip={}):
        """
        Send a message to all connected clients, except those in skip

        Args:
            response (Response): Response to send to all connections
            skip (set, optional): Union[Websocket, Iterable[Websocket]] to skip. Defaults to {}.
        """
        if not isinstance(skip, Iterable):
            skip = {skip}

        for websocket in self.connected:
            if websocket not in skip:
                await self.send(response, websocket)

    @log(logger, logging.CRITICAL)
    async def handle_shutdown(self):
        """
        Notifies all clients of shutdown and closes their connections
        """
        await self.send_to_all(Response(self.get_shutdown_notification(), Origin.SERVER))
        for conn in self.connected.keys():
            await conn.close()

    @log(logger, logging.INFO)
    async def change_name(self, websocket, new_name):
        """
        Changes name of user connected with websocket to new_name

        Args:
            websocket (Websocket): connection to change name of
            new_name (str): new name for user
        """
        old_name = self.connected[websocket].name

        # sanitize by removing all whitespace
        new_name = "".join(new_name.split())

        self.connected[websocket].name = new_name
        await self.send_to_all(Response(self.get_name_change_notification(old_name, new_name), Origin.SERVER))

    @log(logger, logging.INFO)
    async def private_message(self, message, from_websocket, to_websocket):
        outgoing = Response(self.get_outgoing_pm(message, self.connected[from_websocket].name), Origin.PRIVATE)
        receipt = Response(self.get_pm_receipt(message, self.connected[to_websocket].name), Origin.PRIVATE)

        await self.send(outgoing, to_websocket)
        await self.send(receipt, from_websocket)

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

    def get_outgoing_pm(self, message, from_name):
        return Template(self.config["private_messate_from_temp"]).substitute(from_name=from_name, message=message)

    def get_pm_receipt(self, message, to_name):
        return Template(self.config["private_message_to_temp"]).substitute(to_name=to_name, message=message)

    def __repr__(self):
        return f"<Chatroom, connections: {len(self.connected)}>"


class AdjAnimalNameGenerator:

    def __init__(self, adj_path, animal_path):
        with open(adj_path) as adjs:
            self.adjectives = [word.strip().capitalize()
                               for word in adjs.readlines()]
        with open(animal_path) as animals:
            self.animals = [word.strip().capitalize()
                            for word in animals.readlines()]

    def generate_name(self):
        return f"{random.choice(self.adjectives)}{random.choice(self.animals)}"
