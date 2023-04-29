from collections import namedtuple
from os import getenv

import openai
from dotenv import load_dotenv

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

token = getenv("OPENAI_TOKEN")
model = getenv("OPENAI_MODEL")
prompt = Message("system", getenv("OPENAI_SYSTEM_MESSAGE"))
conversation = [prompt]

openai.api_key = token


def next_message(text: str) -> str:
    new_message = Message("user", text)
    message_list = [message._asdict() for message in [*conversation, new_message]]
    response = openai.ChatCompletion.create(model=model, messages=message_list)
    conversation.append(new_message)
    response_message = _parse_response(response)
    conversation.append(response_message)
    return response_message.content


def _parse_response(response) -> Message:
    message = response["choices"][0]["message"]
    content = message["content"]
    role = message["role"]
    return Message(role, content)


def reset_conversation() -> None:
    conversation.clear()
    conversation.append(prompt)
