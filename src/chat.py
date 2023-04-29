from collections import defaultdict, namedtuple
from os import getenv

import openai
from dotenv import load_dotenv

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

token = getenv("OPENAI_TOKEN")
model = getenv("OPENAI_MODEL")
system_message = getenv("OPENAI_SYSTEM_MESSAGE")
initial_message = getenv("OPENAI_INITIAL_MESSAGE")
context_limit = getenv("OPENAI_CONTEXT_LIMIT")
context_limit = int(context_limit) if context_limit else None

prompt = [Message("system", system_message)]
if initial_message:
    prompt.append(Message("user", initial_message))
conversations = defaultdict(list)

openai.api_key = token


def next_message(chat_id: int, text: str) -> str:
    conversation = _get_conversation(chat_id)
    new_message = Message("user", text)
    message_list = [message._asdict() for message in [*conversation, new_message]]
    response = openai.ChatCompletion.create(model=model, messages=message_list)
    conversation.append(new_message)
    response_message = _parse_response(response)
    conversation.append(response_message)
    return response_message.content


def reset(chat_id: int) -> None:
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
