# Simple OpenAI text model Discord bot

A simple Discord bot wrapping [OpenAI API](https://openai.com/blog/openai-api/) text models (like [ChatGPT](https://openai.com/blog/chatgpt)), build with [`hikari`](https://github.com/hikari-py/hikari) and [`lightbulb`](https://github.com/tandemdude/hikari-lightbulb)!

Bot works only on servers and won't respond to DMs.

Conversation/context is not stored permanently and will be removed when the bot is restarted.



## Requirements

This bot was built with `Python 3.11`, [`hikari`](https://github.com/hikari-py/hikari), [`lightbulb`](https://github.com/tandemdude/hikari-lightbulb) and [`openai-python`](https://github.com/openai/openai-python).
Full list of Python requirements is in the `requirements.txt` file, you can use it to install all of them.



## Configuration

Configuration is done through a `.env` file. You can copy example file `.env.example` as `.env` and fill required parameters.

```commandline
cp .env.example .env
```


### Discord bot

Only required parameter is a bot token

```dotenv
BOT_TOKEN='<your secret bot token>'
```


### OpenAI API

One required parameter is [API key](https://platform.openai.com/account/api-keys).

```dotenv
OPENAI_TOKEN='<your secret API key>'
```

Through `.env` you can also configure other parameters:
* `OPENAI_MODEL` - which model to use (gpt-3.5-turbo is used by default)
* `OPENAI_SYSTEM_MESSAGE` - system message
* `OPENAI_CONTEXT_LIMIT` - how many messages will be kept in the context aside from prompt, all messages will be kept if empty
* `OPENAI_INITIAL_MESSAGE` - additional message added after system message to all conversations, can be empty for no additional messages

Note that `gpt-3.5-turbo` [doesn't pay strong attention to system message](https://platform.openai.com/docs/guides/chat/instructing-chat-models), so changing it might not provide significant changes to responses.
You can use `OPENAI_INITIAL_MESSAGE` to tweak initial behaviour of the model.

```dotenv
OPENAI_MODEL='gpt-3.5-turbo'
OPENAI_SYSTEM_MESSAGE='You are a helpful assistant.'
OPENAI_CONTEXT_LIMIT=1000
OPENAI_INITIAL_MESSAGE='You are a helpful assistant acting like 18th century butler,'
```


## Commands

All commands work only on servers and aren't available in DMs.

* `/start` - starts responding to all messages in current channel
* `/quiet_start` - starts responding to all messages in current channel without notifying other users
* `/stop` - stops responding to messages
* `/restart` - resets current conversation and removes all context, other than system message
* `/ask` - ask for specific prompt, can be used in channels which aren't actively monitored, guild only
* `ask` - **message command**, can use specified message as prompt
* `/prompt set <prompt text>` - sets custom prompt for this channel
* `/prompt reset` - clears custom prompt for this channel
* `/prompt remove` - remove all prompts, including ones from bot configuration file
* `/prompt get` - get custom prompt, won't return prompt from configuration file to avoid leaking configuration data to users



## Running the bot

You can run the bot from the source code directly, or in a Docker container.


### From source code

1. Create a Discord bot
2. Create [OpenAI API key](https://platform.openai.com/account/api-keys)
3. Install all packages from `requirements.txt`
4. Fill `.env` file
5. Run `main.py` file with Python


### Docker

1. Create a Discord bot
2. Create [OpenAI API key](https://platform.openai.com/account/api-keys)
3. Fill `.env` file
4. Run `docker compose up -d --build` in terminal

Note that `.env` file is used only for loading environment variables into Docker container through compose.
The file itself isn't added to the container.
