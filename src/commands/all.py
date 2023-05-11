from hikari import GuildMessageCreateEvent
from lightbulb import BotApp, Context, Plugin, SlashCommand, add_checks, command, guild_only, implements

from chat import initial_message, next_message, reset_conversation

all_plugin = Plugin("all_plugin")
source_guild_channels = set()


@all_plugin.command()
@add_checks(guild_only)
@command("start", "Start conversation", auto_defer=True)
@implements(SlashCommand)
async def start(context: Context) -> None:
    await _start(initial_message(context.channel_id), context)


@all_plugin.command()
@add_checks(guild_only)
@command("quiet_start", "Start conversation without notifying other users", ephemeral=True)
@implements(SlashCommand)
async def quiet_start(context: Context) -> None:
    await _start("Replying to all messages.", context)


async def _start(message: str, context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    source_guild_channels.add(channel_id)
    await context.respond(message)


@all_plugin.command()
@add_checks(guild_only)
@command("stop", "Stops conversation")
@implements(SlashCommand)
async def stop(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    if channel_id in source_guild_channels:
        source_guild_channels.remove(channel_id)
    await context.respond("Conversation stopped.")


@all_plugin.command()
@add_checks(guild_only)
@command("restart", "Restarts conversation and its context", auto_defer=True)
@implements(SlashCommand)
async def restart(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    await context.respond("Conversation restarted.")
    await start(context)


@all_plugin.listener(event=GuildMessageCreateEvent)
async def on_message(event: GuildMessageCreateEvent) -> None:
    if _should_skip_message(event):
        return
    response = next_message(event.channel_id, event.content)
    await event.message.respond(response)


def _should_skip_message(event: GuildMessageCreateEvent) -> bool:
    return (
            not event.is_human
            or event.channel_id not in source_guild_channels
            or not event.content
    )


def load(bot: BotApp) -> None:
    bot.add_plugin(all_plugin)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(all_plugin)
