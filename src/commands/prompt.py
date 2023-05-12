from lightbulb import (BotApp, Context, Plugin, SlashCommandGroup, SlashSubCommand, add_checks, command, implements,
                       option)

from chat import get_custom_prompt, remove_custom_prompt, remove_prompt, reset_conversation, store_custom_prompt
from command_check import check

prompt_plugin = Plugin("prompt_plugin")


@prompt_plugin.command()
@add_checks(check)
@command("prompt", "Command group related to forced prompts")
@implements(SlashCommandGroup)
async def prompt_group(_: Context) -> None:
    pass


@prompt_group.child()
@add_checks(check)
@option("prompt", "New custom prompt", str)
@command("set", "Set custom prompt for this channel")
@implements(SlashSubCommand)
async def prompt_set(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    new_prompt = context.options.prompt
    store_custom_prompt(channel_id, new_prompt)
    await context.respond(f"Prompt set to: **{new_prompt}**")


@prompt_group.child()
@add_checks(check)
@command("reset", "Reset custom prompt for this channel to default")
@implements(SlashSubCommand)
async def prompt_reset(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    remove_custom_prompt(channel_id)
    await context.respond("Prompt reset.")


@prompt_group.child()
@add_checks(check)
@command("get", "Get current custom prompt")
@implements(SlashSubCommand)
async def prompt_get(context: Context) -> None:
    channel_id = context.channel_id
    custom_prompt = get_custom_prompt(channel_id)
    await context.respond(f"Prompt set to: **{custom_prompt}**" if custom_prompt else "No custom prompt configured.")


@prompt_group.child()
@add_checks(check)
@command("remove", "Remove custom prompt for this channel")
@implements(SlashSubCommand)
async def prompt_remove(context: Context) -> None:
    channel_id = context.channel_id
    reset_conversation(channel_id)
    remove_prompt(channel_id)
    await context.respond("Prompt removed.")


def load(bot: BotApp) -> None:
    bot.add_plugin(prompt_plugin)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(prompt_plugin)
