from collections import defaultdict, namedtuple
from os import getenv

import openai
from dotenv import load_dotenv
from openai.error import RateLimitError

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

TOKEN = getenv("OPENAI_TOKEN")
MODEL = getenv("OPENAI_MODEL")
SYSTEM_MESSAGE = getenv("OPENAI_SYSTEM_MESSAGE")
INITIAL_MESSAGE = getenv("OPENAI_INITIAL_MESSAGE")
CONTEXT_LIMIT = getenv("OPENAI_CONTEXT_LIMIT")

initial_prompt = [Message("system", SYSTEM_MESSAGE)]
if INITIAL_MESSAGE:
    initial_prompt.append(Message("user", INITIAL_MESSAGE))
conversations = defaultdict(list)
custom_prompts = defaultdict(lambda: initial_prompt)

openai.api_key = TOKEN


def initial_message() -> str | None:
    messages = [message._asdict() for message in initial_prompt]
    response = _get_response(messages)
    if not response:
        return None
    response_message = _parse_response(response)
    return response_message.content


def next_message(channel_id: int, text: str) -> str | None:
    conversation = conversations[channel_id]
    new_message = Message("user", text)
    messages = [message._asdict() for message in [*custom_prompts[channel_id], *conversation, new_message]]
    response = _get_response(messages)
    if not response:
        return None
    _store_message(conversation, new_message)
    response_message = _parse_response(response)
    _store_message(conversation, response_message)
    return response_message.content


def reset_conversation(channel_id: int) -> None:
    conversations.pop(channel_id, None)


def store_custom_prompt(channel_id: int, prompt: str) -> None:
    custom_prompts[channel_id] = [Message("system", prompt), Message("user", prompt)]


def remove_custom_prompt(channel_id: int) -> None:
    if channel_id in custom_prompts:
        custom_prompts.pop(channel_id, None)


def _get_response(messages: list[dict[str, str]]):
    try:
        return openai.ChatCompletion.create(model=MODEL, messages=messages)
    except RateLimitError:
        return None


def _store_message(conversation: list[Message], message: Message) -> None:
    conversation.append(message)
    if CONTEXT_LIMIT and len(conversation) > int(CONTEXT_LIMIT):
        conversation.pop(0)


def _parse_response(response) -> Message:
    message = response["choices"][0]["message"]
    content = message["content"]
    role = message["role"]
    return Message(role, content)
