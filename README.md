# Quran Recitation Collection Bot

## 1. What this bot does

This Telegram bot collects Quran recitations from users as voice messages or audio files. Each accepted submission is forwarded instantly to one designated Telegram group for admins to review there, without sending direct messages to individual admins.

## 2. Prerequisites

- Python 3.11 installed locally
- A Telegram bot token from BotFather
- A Telegram group where all recitations will be forwarded
- Permission to add the bot to that group and grant it posting rights

## 3. Getting BOT_TOKEN from BotFather

1. Open Telegram and search for `@BotFather`.
2. Start a chat with BotFather and send `/newbot`.
3. Follow the prompts to choose a bot name and a unique bot username.
4. BotFather will send you an API token.
5. Copy that token and use it as the value for `BOT_TOKEN` in your `.env` file or Railway variables.

## 4. Getting ADMIN_GROUP_ID

1. Create your Telegram group if you have not already done so.
2. Add `@RawDataBot` to the group.
3. Send any new message in the group after adding `@RawDataBot`.
4. `@RawDataBot` will print the raw update data, including the group ID.
5. Copy the group ID and use it as `ADMIN_GROUP_ID`. It will be a negative number, usually starting with `-100`.

## 5. Adding the bot to the group and granting it "Post Messages" admin permission

1. Add your bot to the target Telegram group.
2. Open the group settings and promote the bot to an admin.
3. Grant the bot the permission to post messages in the group.
4. Save the group settings.
5. Keep the bot in that group so it can forward all user submissions there.

## 6. Local setup: copy .env.example → .env → fill values → pip install -r requirements.txt → python bot.py

1. Open a terminal in the project folder.
2. Copy `.env.example` to `.env`.
3. Fill in `BOT_TOKEN`, `ADMIN_GROUP_ID`, and optionally `MAX_SUBMISSIONS`.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the bot:

   ```bash
   python bot.py
   ```

## 7. Railway deployment step by step

1. Push this code to a GitHub repository.
2. Go to [railway.app](https://railway.app) and create a new project.
3. Choose **New Project** and then **Deploy from GitHub repo**.
4. Select the repository that contains this bot.
5. Open the **Variables** tab in Railway.
6. Add these variables:
   - `BOT_TOKEN`
   - `ADMIN_GROUP_ID`
   - `MAX_SUBMISSIONS`
7. Railway will detect the `Procfile` and deploy automatically.
8. After deployment, confirm the worker starts successfully in the Railway logs.
9. Important: SQLite is ephemeral on Railway and resets on redeploy or container replacement. For persistent logs, upgrade to Railway's PostgreSQL plugin and adapt `db.py` accordingly.
