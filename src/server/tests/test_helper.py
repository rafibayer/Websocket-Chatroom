import logging
import asyncio

# supress test logging
logging.disable(logging.CRITICAL)


def sync(awaitable):
    return asyncio.get_event_loop().run_until_complete(awaitable)