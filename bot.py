from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
import datetime

# ⚠️ REPLACE THIS WITH YOUR REAL TOKEN
TOKEN = "8768265670:AAE9lLWyJXUuOyoYA-BkLaQ_hisE4mRa_10" 

# ⚠️ REPLACE THIS WITH YOUR ACTUAL GROUP CHAT ID (e.g., -100123456789)
GROUP_CHAT_ID = 0 

people = [
    "Abrham",
    "Abu",
    "Hilina",
    "Bisrat",
    "Bisrat T",
    "Nafyad",
    "Bezawit"
]

def get_today_payer():
    today = datetime.date.today()
    start = datetime.date(2024, 1, 1)  
    diff = (today - start).days
    index = diff % len(people)
    return people[index]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ticket Bot Active 🎟️\nUse /today to see who pays today."
    )

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payer = get_today_payer()
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"Today's ticket payer: {payer}\nThis group ID is: {chat_id}"
    )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    payer = get_today_payer()
    try:
        await context.application.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"Reminder 🚨\nToday's ticket payer is: {payer}"
        )
    except Exception as e:
        print(f"Failed to send reminder: {e}")

# Build the application
app = ApplicationBuilder().token(TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))

# Add daily job (8:00 AM)
app.job_queue.run_daily(send_reminder, time=datetime.time(8, 0))

print("Bot is running...")

# Run polling directly (no asyncio.run needed)
app.run_polling()