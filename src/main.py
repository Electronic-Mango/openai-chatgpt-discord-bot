from logging import INFO, basicConfig
from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from chat import initial_message, next_message, reset_conversation
from rate_error_handler import rate_error_handler

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    talk_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), talk)
    application.add_handler(talk_handler)
    reset_handler = CommandHandler("reset", reset)
    application.add_handler(reset_handler)

    application.add_error_handler(rate_error_handler)

    application.run_polling()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = initial_message()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    response = next_message(chat_id, update.message.text)
    await context.bot.send_message(chat_id=chat_id, text=response)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Conversation restarted.")
    await start(update, context)


if __name__ == "__main__":
    main()
