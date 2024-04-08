from collections import defaultdict, namedtuple
from os import getenv

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

Message = namedtuple("Message", ["role", "content"])

RATE_LIMIT_MESSAGE = "Rate limit reached, try again in 20s."

TOKEN = getenv("OPENAI_TOKEN")
MODEL = getenv("OPENAI_MODEL")
SYSTEM_MESSAGE = getenv("OPENAI_SYSTEM_MESSAGE")
INITIAL_MESSAGE = getenv("OPENAI_INITIAL_MESSAGE")
CONTEXT_LIMIT = getenv("OPENAI_CONTEXT_LIMIT")

initial_prompt = [Message("system", SYSTEM_MESSAGE), Message("user", INITIAL_MESSAGE)]
conversations = defaultdict(list)
custom_prompts = defaultdict(lambda: initial_prompt)

client = OpenAI(api_key=TOKEN)


def initial_message(channel_id: int) -> str | None:
    return next_message(channel_id, "Show a welcome message explaining who you are and what you can do.", False)


def next_message(channel_id: int, text: str, use_conversation: bool = True) -> str:
    prompt = custom_prompts[channel_id]
    conversation = conversations[channel_id] if use_conversation else []
    new_message = Message("user", text)
    messages = [message._asdict() for message in [*prompt, *conversation, new_message] if message.content]
    response = _get_response(messages)
    if not response:
        return RATE_LIMIT_MESSAGE
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


def remove_prompt(channel_id: int) -> None:
    store_custom_prompt(channel_id, None)


def get_custom_prompt(channel_id: int) -> str | None:
    return custom_prompts[channel_id][-1].content if channel_id in custom_prompts else None


def _get_response(messages: list[dict[str, str]]):
    try:
        return client.chat.completions.create(model=MODEL, messages=messages)
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
