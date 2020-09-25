import asyncio
import re
from utils import logged

def register(command, dict):
    """
    Decorator factory, decorator registers a function as a command in a given dict

    Args:
        command (str): string to invoke command
        dict (dict): dictionary to register commands in
    """
    def decorator(func):
        dict[command] = func
        return func
    return decorator

registered = dict()

class CommandHandler:

    def __init__(self, pattern = "^!.+"):
        """
        Create a new command handler

        Args:
            pattern (str, optional): regex pattern for a command. Defaults to "^!.+".
        """
        self._regex = re.compile(pattern)
        self.registered_commands = registered

    def is_command(self, message):
        """
        returns whether a given message is a command

        Args:
            message (str): message

        Returns:
            bool: whether message is a command
        """
        return self._regex.match(message) is not None

    @logged
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
            await user.websocket.send(f"\"{command_message}\" is not a valid command (Syntax)")
            return        
        command_name, command_args = self._parse_command(command_message)
        if command_name not in self.registered_commands:
            await user.websocket.send(f"\"{command_message}\" is not a valid command (Doesn't exist)")
            return

        command_func = self.registered_commands[command_name]
        await command_func(self, user, chatroom, command_args)

    def _parse_command(self, command_str):
        """
        Extracts name and args from a command string, assumes command_str is a command

        Args:
            command_str (str): valid command possibly followed by args

        Returns:
            Tuple[str, List[str]]: command name, and list of 0 or more args
        """
        split = command_str.split()
        return split[0].lower(), split[1:]

    @register("!help", registered)
    async def help(self, user, chatroom, args):
        """
        Help command, sends user information about availible commands

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
        response = f"Here are some commands you can use:\n\t{', '.join(self.registered_commands.keys())}"
        await user.websocket.send(response)

    @register("!about", registered)
    async def info(self, user, chatroom, args):
        """
        Info command, sends user information about chatroom

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
        response = f"This is a websocket-based, in-memory, chatroom written in Python by Rafi Bayer (github.com/rafibayer)"
        await user.websocket.send(response)

    @register("!setname", registered)
    async def setname(self, user, chatroom, args):
        """
        Setname command, allows user to change their name

        Args:
            user (User): user who called the command
            chatroom (Chatroom): chatroom in which the command was called
            args (List[str]): command args
        """
        new_name = "".join(args)
        if len(new_name) < 1:
            await user.websocket.send(f"!setname usage is \"!setname <new name>\"")
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
        resp = f"Connected Users: {everyone}"
        await user.websocket.send(resp)


