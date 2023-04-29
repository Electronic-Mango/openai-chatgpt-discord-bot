from os import getenv

from dotenv import load_dotenv
from hikari import DMMessageCreateEvent, Intents, MessageCreateEvent
from lightbulb import BotApp, Context, PrefixCommand, SlashCommand, add_checks, command, guild_only, implements

from chat import initial_message, next_message, reset_conversation

load_dotenv()

token = getenv("BOT_TOKEN")
bot = BotApp(token=token, intents=Intents.ALL, prefix="!")
source_channel = None


@bot.command()
@add_checks(guild_only)
@command("start", "Start conversation", auto_defer=True)
@implements(SlashCommand, PrefixCommand)
async def start(context: Context) -> None:
    _reset_conversation_and_set_channel(context.channel_id)
    message = initial_message()
    await context.respond(message)


@bot.command()
@add_checks(guild_only)
@command("stop", "Stops conversation")
@implements(SlashCommand, PrefixCommand)
async def stop(context: Context) -> None:
    _reset_conversation_and_set_channel(None)
    await context.respond("Conversation stopped.")


@bot.command()
@command("restart", "Restarts conversation and its context", auto_defer=True)
@implements(SlashCommand, PrefixCommand)
async def restart(context: Context) -> None:
    _reset_conversation_and_set_channel(context.channel_id)
    await context.respond("Conversation restarted.")
    await start(context)


def _reset_conversation_and_set_channel(channel: int | None) -> None:
    reset_conversation(0)
    global source_channel
    source_channel = channel


@bot.listen()
async def on_message(event: MessageCreateEvent) -> None:
    if _should_skip_message(event):
        return
    response = next_message(0, event.content)
    await event.message.respond(response)


def _should_skip_message(event: MessageCreateEvent) -> bool:
    if not event.is_human or event.content[0] == "!":
        return True
    if isinstance(event, DMMessageCreateEvent):
        return False
    return event.channel_id != source_channel


bot.run()
