from lightbulb import BotApp, Context, Plugin, SlashCommand, add_checks, command, implements, option
from lightbulb.commands import MessageCommand

from chat import next_message
from command_check import check
from sender import send

ask_plugin = Plugin("ask_plugin")


@ask_plugin.command()
@option("query", "Text to ask", str)
@add_checks(check)
@command("ask", "Ask for specific thing", auto_defer=True)
@implements(SlashCommand)
async def ask(context: Context) -> None:
    response = next_message(context.channel_id, context.options.query)
    await send(response, context.respond)


@ask_plugin.command()
@add_checks(check)
@command("ask", "Ask for specific thing", auto_defer=True)
@implements(MessageCommand)
async def ask_directly(context: Context) -> None:
    response = next_message(context.channel_id, context.options.target.content)
    await send(response, context.respond)


def load(bot: BotApp) -> None:
    bot.add_plugin(ask_plugin)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(ask_plugin)
