import asyncio
import websockets
from chatroom import Chatroom
from utils import logged

class Server:

    @logged
    def __init__(self, host, port):
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

    @logged
    def start(self):
        """
        Starts the server
        """
        start_server_async = websockets.serve(self.ws_handler_async, self.host, self.port)
        self.running = True
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
                await self.chatroom.handle_message(websocket, message)
        finally:

            # websocket disconnects
            await self.chatroom.handle_disconnect(websocket)

    def __str__(self):
        return f"Server @{self.host}:{self.port}, running: {self.running}, Chatroom: \n\t{str(self.chatroom)}"

if __name__ == "__main__":
    s = Server("localhost", 5000)
    print(s)
    s.start()