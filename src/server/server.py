import asyncio
import websockets
from chatroom import Chatroom

# websocket server for chatroom, recieves incoming connections, messages, and disconnects
class Server:

    # create a new server at a given host and port
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.chatroom = Chatroom()

    # start server event loop
    def start(self):
        print(f"Starting server at {self.host}:{self.port}...")
        start_server_async = websockets.serve(self.server_async, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server_async)
        asyncio.get_event_loop().run_forever()

    # server event loop
    async def server_async(self, websocket, path):

        # new connection
        await self.chatroom.handle_connection(websocket)
        try:

            # message in connection
            async for message in websocket:
                await self.chatroom.handle_message(websocket, message)
        finally:

            # websocket disconnects
            await self.chatroom.handle_disconnect(websocket)

if __name__ == "__main__":
    s = Server("localhost", 5000)
    s.start()