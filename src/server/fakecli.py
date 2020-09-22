import asyncio
import websockets

URI =  "ws://localhost:5000"

async def hello():
    async with websockets.connect(URI) as websocket:
        while True:
            message = input("msg: ")

            await websocket.send(message)
            print(f"> {message}")

            resp = await websocket.recv()
            print(f"< {resp}")

asyncio.get_event_loop().run_until_complete(hello())