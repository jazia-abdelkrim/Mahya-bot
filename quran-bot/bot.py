import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from db import init_db
from handlers.start import start_command
from handlers.voice import handle_invalid_submission, handle_recitation


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def build_application() -> Application:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler(["start", "help"], start_command))
    application.add_handler(
        MessageHandler(filters.VOICE | filters.AUDIO, handle_recitation)
    )
    application.add_handler(
        MessageHandler(
            filters.ALL
            & ~filters.COMMAND
            & ~(filters.VOICE | filters.AUDIO),
            handle_invalid_submission,
        )
    )

    return application


def main() -> None:
    logger.info("Initializing database")
    init_db()

    logger.info("Starting Quran Recitation Collection Bot")
    application = build_application()
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
