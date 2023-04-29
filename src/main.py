from os import getenv

from dotenv import load_dotenv
from hikari import GatewayBot, Intents, MessageCreateEvent

import chat

load_dotenv()

token = getenv("BOT_TOKEN")
bot = GatewayBot(token=token, intents=Intents.ALL)


@bot.listen()
async def on_message(event: MessageCreateEvent) -> None:
    if not event.is_human:
        return
    response = chat.next_message(event.content)
    await event.message.respond(response)


bot.run()
