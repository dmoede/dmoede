import json
import logging
import os
import random
from datetime import time

import pytz
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from questions import QUESTIONS

BOT_TOKEN = "8717912049:AAFtBLWYpEmgHSk6RmB4QFuIHSi0-7e3yp8"
DATA_FILE = "data.json"
MOUNTAIN_TZ = pytz.timezone("America/Denver")
QUIZ_HOUR = 18
QUIZ_MINUTE = 0

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}


def save_data(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user(data: dict, chat_id: int) -> dict:
    cid = str(chat_id)
    if cid not in data:
        data[cid] = {
            "score": 0,
            "streak": 0,
            "total": 0,
            "current_question": None,
            "used_questions": [],
        }
    return data[cid]


def pick_question(user: dict) -> dict:
    used = set(user["used_questions"])
    available = [i for i in range(len(QUESTIONS)) if i not in used]
    if not available:
        user["used_questions"] = []
        available = list(range(len(QUESTIONS)))
    idx = random.choice(available)
    user["used_questions"].append(idx)
    return QUESTIONS[idx], idx


def format_question(q: dict) -> str:
    text = f"🤖 *Quiz Time\\!*\n\n{escape(q['question'])}"
    if q["type"] == "mc":
        text += "\n\n" + "\n".join(escape(o) for o in q["options"])
        text += "\n\n_Reply with_ *A*, *B*, *C*, or *D*"
    elif q["type"] == "tf":
        text += "\n\n_Reply with_ *True* or *False*"
    return text


def escape(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    for ch in r"_*[]()~`>#+-=|{}.!":
        text = text.replace(ch, f"\\{ch}")
    return text


def check_answer(q: dict, user_answer: str) -> bool:
    answer = user_answer.strip().upper()
    correct = q["answer"].upper()
    if q["type"] == "mc":
        return answer == correct or answer == correct[0]
    elif q["type"] == "tf":
        if "TRUE" in answer:
            return correct == "TRUE"
        if "FALSE" in answer:
            return correct == "FALSE"
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    data = load_data()
    get_user(data, chat_id)
    save_data(data)

    # Remove any existing daily job for this user, then re-add
    for job in context.job_queue.get_jobs_by_name(f"daily_{chat_id}"):
        job.schedule_removal()

    context.job_queue.run_daily(
        send_daily_quiz,
        time=time(hour=QUIZ_HOUR, minute=QUIZ_MINUTE, tzinfo=MOUNTAIN_TZ),
        chat_id=chat_id,
        name=f"daily_{chat_id}",
    )

    await update.message.reply_text(
        "👋 Welcome to *AI Quiz Bot\\!*\n\n"
        "I'll send you one AI question every day at *6 PM Mountain Time*\\.\n\n"
        "You can also ask for a question any time:\n\n"
        "/quiz — Get a question right now\n"
        "/score — See your score and streak\n"
        "/stop — Pause daily questions",
        parse_mode="MarkdownV2",
    )


async def send_daily_quiz(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id
    data = load_data()
    user = get_user(data, chat_id)
    q, idx = pick_question(user)
    user["current_question"] = idx
    save_data(data)

    await context.bot.send_message(
        chat_id=chat_id,
        text=format_question(q),
        parse_mode="MarkdownV2",
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    data = load_data()
    user = get_user(data, chat_id)
    q, idx = pick_question(user)
    user["current_question"] = idx
    save_data(data)
    await update.message.reply_text(format_question(q), parse_mode="MarkdownV2")


async def score(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    data = load_data()
    user = get_user(data, chat_id)
    total = user["total"]
    correct = user["score"]
    streak = user["streak"]
    pct = int(correct / total * 100) if total > 0 else 0
    streak_emoji = "🔥" if streak >= 3 else "📈" if streak >= 1 else "💤"
    await update.message.reply_text(
        f"*Your Stats*\n\n"
        f"✅ Correct: {correct}/{total} \\({pct}%\\)\n"
        f"{streak_emoji} Streak: {streak} day{'s' if streak != 1 else ''} in a row",
        parse_mode="MarkdownV2",
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    for job in context.job_queue.get_jobs_by_name(f"daily_{chat_id}"):
        job.schedule_removal()
    await update.message.reply_text(
        "Daily questions paused\\. Send /start any time to re\\-subscribe\\.",
        parse_mode="MarkdownV2",
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    data = load_data()
    user = get_user(data, chat_id)

    if user["current_question"] is None:
        await update.message.reply_text(
            "No active question\\! Send /quiz to get one\\.",
            parse_mode="MarkdownV2",
        )
        return

    q = QUESTIONS[user["current_question"]]
    is_correct = check_answer(q, update.message.text)

    user["total"] += 1
    if is_correct:
        user["score"] += 1
        user["streak"] += 1
        header = "✅ *Correct\\!*"
    else:
        user["streak"] = 0
        header = f"❌ *Not quite\\.* The answer is *{escape(q['answer'])}*\\."

    user["current_question"] = None
    save_data(data)

    explanation = escape(q["explanation"])
    pct = int(user["score"] / user["total"] * 100)

    await update.message.reply_text(
        f"{header}\n\n_{explanation}_\n\n"
        f"📊 Score: {user['score']}/{user['total']} \\({pct}%\\) \\| Streak: {user['streak']} 🔥",
        parse_mode="MarkdownV2",
    )


def restore_daily_jobs(app: Application) -> None:
    """Re-schedule daily quizzes for all registered users on startup."""
    data = load_data()
    for chat_id_str in data:
        chat_id = int(chat_id_str)
        app.job_queue.run_daily(
            send_daily_quiz,
            time=time(hour=QUIZ_HOUR, minute=QUIZ_MINUTE, tzinfo=MOUNTAIN_TZ),
            chat_id=chat_id,
            name=f"daily_{chat_id}",
        )
        logger.info(f"Restored daily quiz job for chat_id={chat_id}")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    restore_daily_jobs(app)

    logger.info("Bot is running — press Ctrl+C to stop.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
