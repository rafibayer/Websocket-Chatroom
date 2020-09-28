"""
command_handler allows clients to invoke registered commands via messages
"""
import asyncio
import re
import logging
from response import Response, Origin
from utils import log, log_message

logger = logging.getLogger(__name__)


def register(command, command_dict):
    """
    Decorator factory, decorator registers a function as a command in a given dict

    Args:
        command (str): string used to invoke command
        dict (dict): dictionary to register commands in
    """
    def decorator(func):
        command_dict[command] = func
        return func
    return decorator


registered = dict()


class CommandHandler:

    def __init__(self, pattern="^!.+"):
        """
        Create a new command handler

        Args:
            pattern (str, optional): regex pattern for a command. Defaults to "^!.+".
        """
        self._regex = re.compile(pattern)
        self.registered_commands = registered
        log_message(logger, f"Registered Commands: {self.registered_commands.keys()}", logging.INFO)

    def is_command(self, message):
        """
        returns whether a given message is a command

        Args:
            message (str): message

        Returns:
            bool: whether message is a command
        """
        return self._regex.match(message) is not None

    @log(logger, logging.INFO)
    async def handle_command(self, command_message, user, chatroom):
        """
        Handles a command message from a user in a chatroom

        Args:
            command_message (str): command message
            user (User): chatroom user who sent command
            chatroom (Chatroom): room in which the message was sent
        """
        command_message = command_message.strip()
        if not self.is_command(command_message):
            # occurs when command is invalid after trimming (may have technically been valid before e.x. '!  ')
            resp = Response(f"\"{command_message}\" is not a valid command (Syntax)", Origin.SERVER)
            await chatroom.send(resp, user.websocket)
            return

        command_name, command_args = self._parse_command(command_message)
        if command_name not in self.registered_commands:
            resp = Response(f"\"{command_message}\" is not a valid command (Doesn't exist)", Origin.SERVER)
            await chatroom.send(resp, user.websocket)
            return

        # Invoke the command, passing calling user, chatroom, and arguments
        command_func = self.registered_commands[command_name]
        await command_func(self, user, chatroom, command_args)

    def _parse_command(self, command_str):
        """
        Extracts name and args from a command string, assumes command_str is a command

        Args:
            command_str (str): valid command possibly followed by args

        Returns:
            Tuple[str, str]: command name, command args
        """
        split = command_str.split(maxsplit=1)
        if len(split) == 1:
            return split[0], ""
        else:
            return split[0].lower(), split[1]

    @register("!help", registered)
    async def help(self, user, chatroom, args):
        """
        Help command, sends user information about availible commands

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
       
        body = f"Here are some commands you can use:\n\t{', '.join(self.registered_commands.keys())}"
        resp = Response(body, Origin.SERVER)
        await chatroom.send(resp, user.websocket)

    @register("!about", registered)
    async def info(self, user, chatroom, args):
        """
        Info command, sends user information about chatroom

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
        body = f"This is a websocket-based, in-memory, chatroom created by Rafi Bayer (github.com/rafibayer)"
        resp = Response(body, Origin.SERVER)
        await chatroom.send(resp, user.websocket)

    @register("!setname", registered)
    async def setname(self, user, chatroom, args):
        """
        Setname command, allows user to change their name

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args: <new-username>
        """
        new_name = args
        if len(new_name) < 1:
            resp = Response(f"!setname usage: \"!setname <new name>\"", Origin.SERVER)
            await chatroom.send(resp, user.websocket)
            return
        await chatroom.change_name(user.websocket, new_name)

    @register("!who", registered)
    async def who(self, user, chatroom, args):
        """
        Who command, allows user to see who is connected

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
        everyone = ", ".join([user.name for user in chatroom.connected.values()])
        resp = Response(f"Connected Users: {everyone}", Origin.SERVER)
        await chatroom.send(resp, user.websocket)

    @register("!env", registered)
    async def env(self, user, chatroom, args):
        """Env command, allows client to see what server envionrment they are talking to

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
        resp = Response(f"Enviornment: {chatroom.env}", Origin.SERVER)
        await chatroom.send(resp, user.websocket)

    @register("!ping", registered)
    async def ping(self, user, chatroom, args):
        """Ping command, responds with pong!

        Args:
        user (User): user who called the command
        chatroom (Chatroom): chatroom in which the command was called
        args (List[str]): command args
        """
        resp = Response("pong!", Origin.SERVER)
        await chatroom.send(resp, user.websocket)

    @register("!pm", registered)
    async def pm(self, user, chatroom, args):
        """Private message command, allows a user to send a private message

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (str): command args: <Target-User> <Message Body>
        """
        # Check if user passed any args
        if args == "":
            resp = Response(f"!pm usage: !pm <user> <message>", Origin.SERVER)
            await chatroom.send(resp, user.websocket)
            return

        # split and unpack message (empty if no message)
        target, *message = args.split(maxsplit=1)
        if not message:
            resp = Response(f"!pm usage: !pm <user> <message>", Origin.SERVER)
            await chatroom.send(resp, user.websocket)
            return

        # message should be a list with 1 element after unpacking
        message = message[0]

        # search for target user and send
        for websocket in chatroom.connected:
            target_user = chatroom.connected[websocket]
            if target_user.name == target:
                await chatroom.private_message(message, user.websocket, target_user.websocket)
                return

        # Target user not found
        resp = Response(f"!pm error: user {target} not found", Origin.SERVER)
        await chatroom.send(resp, user.websocket)
