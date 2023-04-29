from os import getenv

from dotenv import load_dotenv
from hikari import Intents, MessageCreateEvent
from lightbulb import BotApp, Context, PrefixCommand, SlashCommand, command, implements

from chat import next_message, reset_conversation

load_dotenv()

token = getenv("BOT_TOKEN")
bot = BotApp(token=token, intents=Intents.ALL, prefix="!")
source_channel = None


@bot.command()
@command("start", "Start conversation")
@implements(SlashCommand, PrefixCommand)
async def start(context: Context) -> None:
    _reset_conversation_and_set_channel(context.channel_id)
    await context.respond("Hello! How may I assist you today?")


@bot.command()
@command("stop", "Stops conversation")
@implements(SlashCommand, PrefixCommand)
async def stop(context: Context) -> None:
    _reset_conversation_and_set_channel(None)
    await context.respond("Conversation stopped.")


@bot.command()
@command("restart", "Restarts conversation and its context")
@implements(SlashCommand, PrefixCommand)
async def restart(context: Context) -> None:
    _reset_conversation_and_set_channel(context.channel_id)
    await context.respond("Conversation restarted.")


def _reset_conversation_and_set_channel(channel: int | None) -> None:
    reset_conversation()
    global source_channel
    source_channel = channel


@bot.listen()
async def on_message(event: MessageCreateEvent) -> None:
    if not event.is_human or event.content[0] == "!" or event.channel_id != source_channel:
        return
    response = next_message(event.content)
    await event.message.respond(response)


bot.run()
