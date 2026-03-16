import logging
from datetime import datetime
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

from telegram.ext import CommandHandler

# Temporary command to get chat ID
# async def chat_id(update, context):
#     chat = update.effective_chat
#     await update.message.reply_text(f"Chat ID: {chat.id}")

BOT_TOKEN = "8736919763:AAF8S6nsVBE_sDRd0JgF-iiMNB2XvTyVFNw"
GROUP_CHAT_ID = "-1003710817280"

members = [
    {"name": "Abu", "username": "abubrhanj"},
    {"name": "Abrsh", "username": "abrsha1"},
    {"name": "Bisrat", "username": "Bbubbles0"},
    {"name": "Hilina", "username": "Hillulu"},
    {"name": "Nafyad", "username": "CarlJohonson"},
    {"name": "Bisrat", "username": "Bisrate_melak"},
    {"name": "Beza", "username": "Bezu3007"},
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def get_today_payer():
    today = datetime.today().weekday()

    if today >= 5:
        return None

    index = today % len(members)
    return members[index]

from datetime import datetime

def get_payer_for_day(day_offset=0):
    today = datetime.today()

    # weekday: 0=Mon, 4=Fri
    weekday = today.weekday() + day_offset

    if weekday >= 5:
        return None

    week_number = today.isocalendar()[1]

    start_index = week_number % len(members)

    index = (start_index + weekday) % len(members)

    return members[index]

async def today(update, context):

    payer = get_payer_for_day(0)

    if payer is None:
        await update.message.reply_text("No lunch today (Weekend 🎉)")
        return

    await update.message.reply_text(
        f"🍽 Today's ticket payer: @{payer['username']} ({payer['name']})"
    )

async def next_payer(update, context):

    payer = get_payer_for_day(1)

    if payer is None:
        await update.message.reply_text("Tomorrow is weekend 🎉")
        return

    await update.message.reply_text(
        f"➡️ Tomorrow's ticket payer: @{payer['username']} ({payer['name']})"
    )


from datetime import datetime, timedelta

async def week(update, context):

    today = datetime.today()

    # find Monday of this week
    monday = today - timedelta(days=today.weekday())

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    message = "📅 Lunch Schedule This Week:\n\n"

    for i, day in enumerate(days):

        payer = get_payer_for_day(i - today.weekday())

        if payer is None:
            continue

        message += f"{day} - @{payer['username']} ({payer['name']})\n"

    await update.message.reply_text(message)

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):

    payer = get_today_payer()

    if payer is None:
        return

    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=f"🍽 Lunch ticket today: @{payer['username']} ({payer['name']})"
    )


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # app.add_handler(CommandHandler("id", chat_id))

    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("next", next_payer))

    app.add_handler(CommandHandler("week", week))

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        send_reminder,
        "cron",
        day_of_week="mon-fri",
        hour=11,
        minute=30,
        args=[app]
    )

    scheduler.start()

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()