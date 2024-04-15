from os import getenv
from pickle import dump, load

from dotenv import load_dotenv

load_dotenv()

SOURCES_FILE = getenv("SOURCES_PERSISTENCE_FILE")


def load_source_channels() -> set[int]:
    if not SOURCES_FILE:
        return set()
    with open(SOURCES_FILE, "rb") as sources:
        return load(sources)


def store_source_channel(channel_id: int) -> None:
    if not SOURCES_FILE:
        return
    existing_sources = load_source_channels()
    existing_sources.add(channel_id)
    with open(SOURCES_FILE, "wb") as sources:
        dump(existing_sources, sources)
