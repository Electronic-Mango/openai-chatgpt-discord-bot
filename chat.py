from collections import defaultdict, namedtuple
from logging import info
from os import getenv

import openai
from dotenv import load_dotenv

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

token = getenv("OPENAI_TOKEN")
model = getenv("OPENAI_MODEL")
prompt = Message("system", getenv("OPENAI_PROMPT"))
conversations = defaultdict(list)

openai.api_key = token


def next_message(chat_id: int, text: str) -> str:
    conversation = _get_conversation(chat_id)
    new_message = Message("user", text)
    message_list = [message._asdict() for message in [*conversation, new_message]]
    response = openai.ChatCompletion.create(model=model, messages=message_list)
    conversation.append(new_message)
    info(response)
    response_message = _parse_response(response)
    conversation.append(response_message)
    return response_message.content


def _get_conversation(chat_id: int) -> list[Message]:
    conversation = conversations[chat_id]
    if not conversation:
        conversation.append(prompt)
    return conversation


def _parse_response(response) -> Message:
    message = response['choices'][0]['message']
    content = message['content']
    role = message['role']
    return Message(role, content)


def reset(chat_id: int) -> None:
    conversations.pop(chat_id)
