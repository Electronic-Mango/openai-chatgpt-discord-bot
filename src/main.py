from os import getenv

from dotenv import load_dotenv
from hikari import Intents, MessageCreateEvent, GuildChannel
from lightbulb import BotApp, command, implements, SlashCommand, Context

from chat import reset, next_message

load_dotenv()

token = getenv("BOT_TOKEN")
bot = BotApp(token=token, intents=Intents.ALL)
source_channel = None


@bot.command()
@command("start", "Start conversation", guilds=(999740151855067216,))
@implements(SlashCommand)
async def start(context: Context) -> None:
    _restart_and_set_channel(context.get_channel())
    await context.respond("Hello! How may I assist you today?")


@bot.command()
@command("stop", "Stops conversation", guilds=(999740151855067216,))
@implements(SlashCommand)
async def stop(context: Context) -> None:
    _restart_and_set_channel(None)
    await context.respond("Conversation stopped.")


@bot.command()
@command("restart", "Restarts conversation and its context", guilds=(999740151855067216,))
@implements(SlashCommand)
async def restart(context: Context) -> None:
    _restart_and_set_channel(context.get_channel())
    await context.respond("Conversation restarted!")


def _restart_and_set_channel(channel: GuildChannel | None) -> None:
    reset()
    global source_channel
    source_channel = channel


@bot.listen()
async def on_message(event: MessageCreateEvent) -> None:
    if not event.is_human or event.get_channel() != source_channel:
        return
    response = next_message(event.content)
    await event.message.respond(response)


bot.run()
