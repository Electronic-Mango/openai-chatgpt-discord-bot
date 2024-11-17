from hikari import MessageCreateEvent
from lightbulb import BotApp, Context, Plugin, SlashCommand, add_checks, command, implements

from attachment_parser import parse_image_urls
from chat import initial_message, next_message, reset_conversation
from command_check import check
from persistence import load_source_channels, store_source_channel
from sender import send

all_plugin = Plugin("all_plugin")
source_channels = load_source_channels()


@all_plugin.command()
@add_checks(check)
@command("start", "Start conversation", auto_defer=True)
@implements(SlashCommand)
async def start(context: Context) -> None:
    start_message = await initial_message(context.channel_id)
    await _start(start_message, context)


@all_plugin.command()
@add_checks(check)
@command("quiet_start", "Start conversation without notifying other users", ephemeral=True)
@implements(SlashCommand)
async def quiet_start(context: Context) -> None:
    await _start("Replying to all messages.", context)


async def _start(message: str, context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    source_channels.add(channel_id)
    store_source_channel(channel_id)
    await send(message, context.respond)


@all_plugin.command()
@add_checks(check)
@command("stop", "Stops conversation")
@implements(SlashCommand)
async def stop(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    if channel_id in source_channels:
        source_channels.remove(channel_id)
    await send("Conversation stopped.", context.respond)


@all_plugin.command()
@add_checks(check)
@command("restart", "Restarts conversation and its context", auto_defer=True)
@implements(SlashCommand)
async def restart(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    await send("Conversation restarted", context.respond)


@all_plugin.listener(event=MessageCreateEvent)
async def on_message(event: MessageCreateEvent) -> None:
    if await _should_skip_message(event):
        return
    channel = await event.message.fetch_channel()
    async with channel.trigger_typing():
        text = event.message.content
        image_urls = parse_image_urls(event.message.attachments)
        response = await next_message(event.channel_id, text, image_urls)
        await send(response, event.message.respond)


async def _should_skip_message(event: MessageCreateEvent) -> bool:
    return not event.is_human or not event.content or event.channel_id not in source_channels


def load(bot: BotApp) -> None:
    bot.add_plugin(all_plugin)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(all_plugin)
