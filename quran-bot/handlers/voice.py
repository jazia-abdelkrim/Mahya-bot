import logging
from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_GROUP_ID, MAX_SUBMISSIONS
from db import get_submission_count, insert_submission, is_duplicate
from messages import DUPLICATE, ERROR_GENERIC, INVALID_TYPE, RATE_LIMITED, THANK_YOU


logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


async def handle_recitation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        message = update.message
        if message is None or message.from_user is None:
            logger.info("Skipping recitation update without message or user")
            return

        if message.voice:
            media = message.voice
            file_type = "voice"
        elif message.audio:
            media = message.audio
            file_type = "audio"
        else:
            await message.reply_text(INVALID_TYPE)
            return

        file_id = media.file_id
        file_unique_id = media.file_unique_id

        if is_duplicate(file_unique_id):
            logger.info("Duplicate submission rejected: %s", file_unique_id)
            await message.reply_text(DUPLICATE)
            return

        user = message.from_user
        full_name = user.full_name
        username = user.username or "no username"
        user_id = user.id

        now_utc = _utc_now()
        window_start = (now_utc - timedelta(hours=24)).isoformat()
        submission_count = get_submission_count(user_id, window_start)

        if submission_count >= MAX_SUBMISSIONS:
            logger.info("Rate limit reached for user_id=%s", user_id)
            await message.reply_text(RATE_LIMITED)
            return

        timestamp_text = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
        caption = (
            "🎙 New recitation\n"
            f"👤 Name: {full_name}\n"
            f"🔖 Username: {'@' + username if user.username else username}\n"
            f"🆔 User ID: {user_id}\n"
            f"📅 {timestamp_text}"
        )

        if file_type == "voice":
            await context.bot.send_voice(
                chat_id=ADMIN_GROUP_ID,
                voice=file_id,
                caption=caption,
            )
        else:
            await context.bot.send_audio(
                chat_id=ADMIN_GROUP_ID,
                audio=file_id,
                caption=caption,
            )

        insert_submission(
            user_id=user_id,
            username=user.username,
            full_name=full_name,
            file_id=file_id,
            file_unique_id=file_unique_id,
            file_type=file_type,
        )

        logger.info(
            "Submission forwarded successfully: user_id=%s file_unique_id=%s",
            user_id,
            file_unique_id,
        )
        await message.reply_text(THANK_YOU)
    except Exception:
        logger.exception("Failed to process voice/audio submission")
        if update.message is not None:
            await update.message.reply_text(ERROR_GENERIC)


async def handle_invalid_submission(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    del context

    try:
        if update.message is None:
            logger.info("Skipping invalid submission response without a message")
            return

        await update.message.reply_text(INVALID_TYPE)
    except Exception:
        logger.exception("Failed to process invalid submission")
        if update.message is not None:
            await update.message.reply_text(ERROR_GENERIC)
