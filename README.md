# Simple OpenAI text model Discord bot

A simple and unofficial Discord bot wrapping [OpenAI API](https://openai.com/blog/openai-api/) text models (like [ChatGPT](https://openai.com/blog/chatgpt)), build with [`hikari`](https://github.com/hikari-py/hikari) and [`lightbulb`](https://github.com/tandemdude/hikari-lightbulb)!

Bot works on servers for everyone, it will respond to DMs only for bot owner.

Configured channel IDs where bot should automatically respond can be stored, the bot will be able to automatically start responding after restart.
Conversation/context is not stored permanently and will be removed when the bot is restarted,
so it won't remember the context of the conversation.



## Requirements

This bot was built with `Python 3.11`, [`hikari`](https://github.com/hikari-py/hikari), [`lightbulb`](https://github.com/tandemdude/hikari-lightbulb) and [`openai-python`](https://github.com/openai/openai-python).
Full list of Python requirements is in the `requirements.txt` file, you can use it to install all of them.



## Bot permissions

### Message content

This bot requires **message content privileged gateway intent** to function correctly.
This is required as bot responds to all messages in a given channel.

You can enable this content for the whole bot in [Discord Developer Portal](https://discord.com/developers/applications) and specific bot settings.

Currently, bot won't even start without this privileged intent enabled.


### Sending text messages

Bot also requires **Send Messages** in **Text permissions**, as it responds with regular messages.



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


You can optionally configure max send message length, by default length of 2000 is used:

```dotenv
MAX_MESSAGE_LENGTH=<custom max message length>
```

If message send by the bot exceeds this value it's split into multiple messages.
2000 is max message length for Discord bots, thus it's used by default.


You can also optionally specify file in which all target channels for `start` command can be stored:

```dotenv
SOURCES_PERSISTENCE_FILE='<path to basic persistence file>'
```

Bot will store all channel IDs where automatic responding is configured in this file.

**It won't store full message conversation.**
After bot is restarted (if the specified file still exists and wasn't modified) it will keep responding in previously configured channels,
however it won't be able to "pick up" the conversation.


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
* `OPENAI_LOG` - log level of OpenAI API, either `debug` or `info`, can be empty for no additional logging configuration

Note that `gpt-3.5-turbo` [doesn't pay strong attention to system message](https://platform.openai.com/docs/guides/chat/instructing-chat-models), so changing it might not provide significant changes to responses.
You can use `OPENAI_INITIAL_MESSAGE` to tweak initial behaviour of the model.

```dotenv
OPENAI_MODEL='gpt-3.5-turbo'
OPENAI_SYSTEM_MESSAGE='You are a helpful assistant.'
OPENAI_CONTEXT_LIMIT=1000
OPENAI_INITIAL_MESSAGE='You are a helpful assistant acting like 18th century butler,'
OPENAI_LOG='info'
```


## Commands

All commands work on servers for everyone and in DMs for bot owner.

* `/start` - starts responding to all messages in current channel
* `/quiet_start` - starts responding to all messages in current channel without notifying other users
* `/stop` - stops responding to messages
* `/restart` - resets current conversation and removes all context, other than system message
* `/ask` - ask for specific prompt, can be used in channels which aren't actively monitored
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

When using Docker the bot will automatically store channel IDs for purposes of `start` command in `persistence` file located in project root.



## Disclaimer

This bot is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with OpenAI.
This is an independent and unofficial project.
Use at your own risk.
