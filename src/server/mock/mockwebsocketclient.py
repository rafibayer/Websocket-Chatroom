import asyncio

class MockWebsocketClient:

    def __init__(self, message="incoming fake message", itr_delay=5):
        self.message = message
        self.delay = itr_delay
        self.open = True
        self.incoming = []

    async def __aiter__(self):
        while True:
            return self.message
            await asyncio.sleep(self.delay)

    async def send(self, message):
        self.incoming.append(message)

    async def recv(self):
        return message

    
