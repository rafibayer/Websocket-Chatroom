import asyncio
import websockets
from chatroom import Chatroom
from utils import logged
from config_manager import ConfigManager

class Server:

    @logged
    def __init__(self, host, port, max_message_len=-1):
        """ 
        Creates a new websocket chatroom server

        Args:
            host (str): Server host
            port (int): Server port
        """
        self.host = host
        self.port = port
        self.running = False
        self.chatroom = Chatroom()
        self.max_message_len = max_message_len

    @logged
    def start(self):
        """
        Starts the server
        """
        self.running = True
        start_server_async = websockets.serve(self.ws_handler_async, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server_async)
        asyncio.get_event_loop().run_forever()

    @logged
    async def ws_handler_async(self, websocket, path):
        """
        Async websocket handler

        Args:
            websocket (Websocket): incoming connection
            path (str): incoming connection resource path
        """

        # new connection
        await self.chatroom.handle_connection(websocket)
        try:

            # message in connection
            async for message in websocket:
                await self.chatroom.handle_message(websocket, message[:self.max_message_len])
        finally:

            # websocket disconnects
            await self.chatroom.handle_disconnect(websocket)

    @logged
    def stop(self):
        asyncio.get_event_loop().stop()
        self.running = False

    def __str__(self):
        return f"Server @{self.host}:{self.port}, running: {self.running}, Chatroom: \n\t{str(self.chatroom)}"

if __name__ == "__main__":
    config = ConfigManager("server/config/server.yaml")
    server_config = config["server"]
    s = Server(server_config["host"], server_config["port"], server_config["max_message_len"])
    print(s)
    s.start()