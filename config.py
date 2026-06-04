import os

from dotenv import load_dotenv


load_dotenv()


def _get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            f"Please set {name} in your environment or .env file."
        )
    return value


BOT_TOKEN = _get_required_env("BOT_TOKEN")

try:
    ADMIN_GROUP_ID = int(_get_required_env("ADMIN_GROUP_ID"))
except ValueError as exc:
    raise ValueError(
        "Invalid ADMIN_GROUP_ID. Please set ADMIN_GROUP_ID to a valid integer "
        "Telegram group ID, such as -1001234567890."
    ) from exc

try:
    MAX_SUBMISSIONS = int(os.getenv("MAX_SUBMISSIONS", "3"))
except ValueError as exc:
    raise ValueError(
        "Invalid MAX_SUBMISSIONS. Please set MAX_SUBMISSIONS to a valid integer."
    ) from exc
