from collections import namedtuple
from logging import info
from os import getenv

import openai
from dotenv import load_dotenv

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

token = getenv("OPENAI_TOKEN")
model = getenv("OPENAI_MODEL")
prompt = Message("system", getenv("OPENAI_PROMPT"))
messages = [prompt]

openai.api_key = token


def next_message(text: str) -> str:
    new_message = Message("user", text)
    messages.append(new_message)
    response = openai.ChatCompletion.create(model=model, messages=[message._asdict() for message in messages])
    info(response)
    response_message = response['choices'][0]['message']
    response_content = response_message['content']
    response_role = response_message['role']
    messages.append(Message(response_role, response_content))
    return response_content


def reset() -> None:
    messages.clear()
    messages.append(prompt)
