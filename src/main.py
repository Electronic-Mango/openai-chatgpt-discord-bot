from os import getenv

from dotenv import load_dotenv
from hikari import Intents
from lightbulb import BotApp

from commands.all import load as load_all
from commands.ask import load as load_ask
from commands.prompt import load as load_prompt

load_dotenv()

INTENTS = Intents.MESSAGE_CONTENT | Intents.DM_MESSAGES | Intents.GUILD_MESSAGES

bot = BotApp(token=getenv("BOT_TOKEN"), intents=INTENTS, logs="DEBUG")

load_all(bot)
load_ask(bot)
load_prompt(bot)

bot.run()
