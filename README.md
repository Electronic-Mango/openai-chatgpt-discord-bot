# Simple OpenAI text model Telegram bot

A simple Telegram bot wrapping [OpenAI API](https://openai.com/blog/openai-api/) text models (like [ChatGPT](https://openai.com/blog/chatgpt)), build with [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)!

Just start a conversation and all messages in the chat will be used as inputs for ChatGPT.

Conversation/context is not stored permanently and will be removed when the bot is restarted.



## Requirements

This bot was built with `Python 3.11`, [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) and [`openai-python`](https://github.com/openai/openai-python).
Full list of Python requirements is in the `requirements.txt` file, you can use it to install all of them.



## Configuration

Configuration is done through a `.env` file. You can copy example file `.env.example` as `.env` and fill required parameters.

```commandline
cp .env.example .env
```


### Telegram bot

Only required parameter is a [bot token](https://core.telegram.org/bots#creating-a-new-bot).

```dotenv
BOT_TOKEN='<your secret bot token>'
```


### OpenAI API

One required parameter is [API key](https://platform.openai.com/account/api-keys).

```dotenv
OPENAI_TOKEN='<your secret API key>'
```

Through `.env` you can also configure which model to use (gpt-3.5-turbo is used by default) and system message.

Note that `gpt-3.5-turbo` [doesn't pay strong attention to system message](https://platform.openai.com/docs/guides/chat/instructing-chat-models), so changing it might not provide significant changes to responses.

```dotenv
OPENAI_MODEL='gpt-3.5-turbo'
OPENAI_SYSTEM_MESSAGE='You are a helpful assistant.'
```


## Commands

* `/start` - prints a basic "hello" message, copied from ChatGPT response
* `/reset` - resets current conversation and removes all context, other than system message



## Running the bot

1. Create a Telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather)
2. Create [OpenAI API key](https://platform.openai.com/account/api-keys)
3. Fill `.env` file
4. Run `main.py` file with Python