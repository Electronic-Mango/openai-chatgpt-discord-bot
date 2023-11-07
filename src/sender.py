from os import getenv
from textwrap import wrap
from typing import Awaitable, Callable

MAX_MESSAGE_LENGTH = int(getenv("MAX_MESSAGE_LENGTH", 2000))


async def send(message: str, sender: Callable[[str], Awaitable[None]]) -> None:
    for partial in wrap(message, MAX_MESSAGE_LENGTH):
        await sender(partial)
