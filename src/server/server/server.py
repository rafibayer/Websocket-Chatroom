import asyncio
import websockets
import logging
from chatroom import Chatroom
from utils import log, log_message
from config_manager import ConfigManager

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, server_config_path, handler):
        """
        Creates a new websocket server

        Args:
            server_config_path (str): path to server configuration
        """
        self.config = ConfigManager(server_config_path)
        self.host = self.config["host"]
        self.port = self.config["port"]
        self.max_message_len = self.config.get("max_message_len", -1)
        self.running = False
        self.handler = handler

    @log(logger, logging.INFO)
    def start(self):
        """
        Starts the server
        """
        self.running = True
        start_server_async = websockets.serve(self.ws_handler_async, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server_async)
        asyncio.get_event_loop().run_forever()

    @log(logger, logging.INFO)
    async def ws_handler_async(self, websocket, path):
        """
        Async websocket handler

        Args:
            websocket (Websocket): incoming connection
            path (str): incoming connection resource path
        """

        # new connection
        await self.handler.handle_connection(websocket)
        try:

            # message in connection
            async for message in websocket:

                # If max_message_len is a valid value, slice message before handling
                if self.max_message_len >= 0:
                    await self.handler.handle_message(websocket, message[:self.max_message_len])
                else:
                    await self.handler.handle_message(websocket, message)

        except websockets.exceptions.ConnectionClosed:

            # Log connection exception
            log_message(logger, f"Exception: ConnectionClosed in websocket {websocket}", logging.WARNING)
        finally:

            # websocket disconnects
            await self.handler.handle_disconnect(websocket)

    @log(logger, logging.CRITICAL)
    async def stop(self):
        """
        Handles a server shutdown, waits for the handler to do whatever it needs to first
        """
        await self.handler.handle_shutdown()
        asyncio.get_event_loop().stop()
        self.running = False
        log_message(logger, "SHUTDOWN COMPLETE", logging.CRITICAL)

    def __str__(self):
        return f"Server @{self.host}:{self.port}, running: {self.running}, Client: \n\t{str(self.handler)}"
