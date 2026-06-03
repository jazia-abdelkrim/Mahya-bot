import logging

from telegram import Update
from telegram.ext import ContextTypes

from messages import ERROR_GENERIC, WELCOME


logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message is None:
            logger.info("Received /start or /help without a message payload")
            return

        await update.message.reply_text(WELCOME)
    except Exception:
        logger.exception("Failed to process /start or /help command")
        if update.message is not None:
            await update.message.reply_text(ERROR_GENERIC)
