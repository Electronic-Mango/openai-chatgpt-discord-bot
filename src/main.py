from os import getenv

from dotenv import load_dotenv
from hikari import GuildMessageCreateEvent, Intents, MessageCreateEvent
from lightbulb import (BotApp, Context, SlashCommand, SlashCommandGroup, SlashSubCommand, add_checks, command,
                       guild_only, implements, option)
from lightbulb.commands import MessageCommand

from chat import (initial_message, next_message, remove_custom_prompt, remove_prompt, reset_conversation,
                  store_custom_prompt, get_custom_prompt)

load_dotenv()

INTENTS = Intents.MESSAGE_CONTENT | Intents.DM_MESSAGES | Intents.GUILD_MESSAGES

bot = BotApp(token=getenv("BOT_TOKEN"), intents=INTENTS)
source_guild_channels = set()


@bot.command()
@add_checks(guild_only)
@command("start", "Start conversation", auto_defer=True)
@implements(SlashCommand)
async def start(context: Context) -> None:
    await _start(initial_message(context.channel_id), context)


@bot.command()
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


@bot.command()
@add_checks(guild_only)
@command("stop", "Stops conversation")
@implements(SlashCommand)
async def stop(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    if channel_id in source_guild_channels:
        source_guild_channels.remove(channel_id)
    await context.respond("Conversation stopped.")


@bot.command()
@add_checks(guild_only)
@command("restart", "Restarts conversation and its context", auto_defer=True)
@implements(SlashCommand)
async def restart(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    await context.respond("Conversation restarted.")
    await start(context)


@bot.command()
@option("query", "Text to ask", str)
@add_checks(guild_only)
@command("ask", "Ask for specific thing", auto_defer=True)
@implements(SlashCommand)
async def ask(context: Context) -> None:
    response = next_message(context.channel_id, context.options.query)
    await context.respond(response)


@bot.command()
@add_checks(guild_only)
@command("ask", "Ask for specific thing", auto_defer=True)
@implements(MessageCommand)
async def ask_directly(context: Context) -> None:
    response = next_message(context.channel_id, context.options.target.content)
    await context.respond(response)


@bot.command
@add_checks(guild_only)
@command("prompt", "Commands related to forced prompts")
@implements(SlashCommandGroup)
async def prompt(_: Context) -> None:
    pass


@prompt.child()
@add_checks(guild_only)
@option("prompt", "New custom prompt", str)
@command("set", "Set custom prompt for this channel")
@implements(SlashSubCommand)
async def prompt_set(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    new_prompt = context.options.prompt
    store_custom_prompt(channel_id, new_prompt)
    await context.respond(f"Prompt set to: **{new_prompt}**")


@prompt.child()
@add_checks(guild_only)
@command("reset", "Reset custom prompt for this channel to default")
@implements(SlashSubCommand)
async def prompt_reset(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    remove_custom_prompt(channel_id)
    await context.respond("Prompt reset.")


@prompt.child()
@add_checks(guild_only)
@command("get", "Get current custom prompt")
@implements(SlashSubCommand)
async def prompt_get(context: Context) -> None:
    channel_id = context.channel_id
    custom_prompt = get_custom_prompt(channel_id)
    await context.respond(f"Prompt set to: **{custom_prompt}**" if custom_prompt else "No custom prompt configured.")


@prompt.child()
@add_checks(guild_only)
@command("remove", "Remove custom prompt for this channel")
@implements(SlashSubCommand)
async def prompt_remove(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    remove_prompt(channel_id)
    await context.respond("Prompt removed.")


@bot.listen()
async def on_message(event: MessageCreateEvent) -> None:
    if _should_skip_message(event):
        return
    response = next_message(event.channel_id, event.content)
    await event.message.respond(response)


def _should_skip_message(event: MessageCreateEvent) -> bool:
    return (
            not event.is_human
            or not isinstance(event, GuildMessageCreateEvent)
            or event.channel_id not in source_guild_channels
            or not event.content
    )


bot.run()
