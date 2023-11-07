from os import getenv
from textwrap import wrap
from typing import Awaitable, Callable

MAX_MESSAGE_LENGTH = int(getenv("MAX_MESSAGE_LENGTH", 2000))


async def send(message: str, sender: Callable[[str], Awaitable[None]]) -> None:
    if len(message) <= MAX_MESSAGE_LENGTH:
        await sender(message.strip())
        return
    parts = wrap(
        message,
        MAX_MESSAGE_LENGTH,
        tabsize=4,
        break_long_words=False,
        replace_whitespace=False,
        break_on_hyphens=False,
        drop_whitespace=False,
    )
    for partial in parts:
        await sender(partial.strip())
