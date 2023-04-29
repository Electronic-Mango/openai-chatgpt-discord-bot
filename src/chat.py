from collections import defaultdict, namedtuple
from os import getenv

import openai
from dotenv import load_dotenv

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

TOKEN = getenv("OPENAI_TOKEN")
MODEL = getenv("OPENAI_MODEL")
SYSTEM_MESSAGE = getenv("OPENAI_SYSTEM_MESSAGE")
INITIAL_MESSAGE = getenv("OPENAI_INITIAL_MESSAGE")
CONTEXT_LIMIT = getenv("OPENAI_CONTEXT_LIMIT")
CONTEXT_LIMIT = int(CONTEXT_LIMIT) if CONTEXT_LIMIT else None

prompt = [Message("system", SYSTEM_MESSAGE)]
if INITIAL_MESSAGE:
    prompt.append(Message("user", INITIAL_MESSAGE))
conversations = defaultdict(list)

openai.api_key = TOKEN


def initial_message() -> str:
    messages = [message._asdict() for message in prompt]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    response_message = _parse_response(response)
    return response_message.content


def next_message(chat_id: int, text: str) -> str:
    conversation = _get_conversation(chat_id)
    new_message = Message("user", text)
    messages = [message._asdict() for message in [*conversation, new_message]]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    conversation.append(new_message)
    response_message = _parse_response(response)
    conversation.append(response_message)
    return response_message.content


def reset_conversation(chat_id: int) -> None:
    conversations.pop(chat_id, None)


def _get_conversation(chat_id: int) -> list[Message]:
    conversation = conversations[chat_id]
    if not conversation:
        conversation.extend(prompt)
    return conversation


def _parse_response(response) -> Message:
    message = response["choices"][0]["message"]
    content = message["content"]
    role = message["role"]
    return Message(role, content)
