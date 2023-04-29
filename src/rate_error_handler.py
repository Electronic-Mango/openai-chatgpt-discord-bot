from openai.error import RateLimitError
from telegram.ext import ContextTypes


async def rate_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = context.error
    message = "Rate limit reached, try again in 20s" if isinstance(error, RateLimitError) else error
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
