import asyncio
import websockets

async def hello():
    uri = "ws://localhost:5000"
    async with websockets.connect(uri) as websocket:
        while True:
            name = input("What's your name? ")

            await websocket.send(name)
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())

# def logger(func):
#     def wrapper(*args, **kwargs):
#         print("wrapper")
#         func(*args, **kwargs)
#     return wrapper

# class test:

#     @logger
#     def t(self, a1, a2, a3="a3"):
#         print(f"{a1=}, {a2=}, {a3=}")

# t = test()
# t.t(1, 2)