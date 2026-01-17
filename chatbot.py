import logging
import requests
import time
import sqlite3

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ===========================
# CONFIGURATION
# ===========================

GEMINI_API_KEYS = [
    "AIzaSyD_dM5ja0CESUCPoDJyUN3jxxzfGEzVaHc",
    "AIzaSyBdkIc7rwc5VyJ07DSXerSLPf4Mt7B3R7I",
    "AIzaSyB1bN3L6hCpHGdry_0Ub4iRfdJ1kKbhqE4"
]

GEMINI_MODEL = "gemini-2.5-flash"
TELEGRAM_BOT_TOKEN = "8537081885:AAEmpmMTfz8CZptBVsXSQuB5UV82Rjl89v4"

EDUCATIONAL_PROMPT = """
Tu es un professeur pour des étudiants.
Réponds uniquement aux questions éducatives sur :
- Mathématiques
- Sciences
- Langues (traduction, grammaire)

Refuse poliment toute autre question.
"""

MAX_RETRIES = 2
DB_NAME = "langue_qcm.db"

# ===========================
# LOGGER
# ===========================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===========================
# MÉMOIRE GEMINI
# ===========================

conversation_history = {}

# ===========================
# BASE DE DONNÉES
# ===========================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        score INTEGER DEFAULT 0,
        question_index INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        niveau TEXT
    );

    CREATE TABLE IF NOT EXISTS choices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        texte TEXT,
        correct INTEGER
    );
    """)

    conn.commit()
    conn.close()

# ===========================
# GEMINI
# ===========================

def ask_gemini(user_id, user_message):
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append(f"Étudiant: {user_message}")
    full_prompt = (
        EDUCATIONAL_PROMPT + "\n" +
        "\n".join(conversation_history[user_id]) +
        "\nProfesseur:"
    )

    for _ in range(MAX_RETRIES):
        for api_key in GEMINI_API_KEYS:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
                response = requests.post(url, json=payload, timeout=10)

                if response.status_code == 200:
                    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    conversation_history[user_id].append(f"Professeur: {reply}")
                    return reply

            except Exception as e:
                logger.error(e)

        time.sleep(1)

    return "⚠️ Problème temporaire avec l’IA."

# ===========================
# LOGIQUE QCM
# ===========================

def get_question(index):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, question FROM questions LIMIT 1 OFFSET ?", (index,))
    q = cursor.fetchone()

    if not q:
        conn.close()
        return None

    cursor.execute("SELECT id, texte FROM choices WHERE question_id=?", (q[0],))
    choices = cursor.fetchall()

    conn.close()
    return q, choices

def estimer_niveau(score):
    if score <= 4:
        return "A1"
    elif score <= 8:
        return "A2"
    elif score <= 13:
        return "B1"
    else:
        return "B2"

# ===========================
# HANDLERS TELEGRAM
# ===========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bonjour !\n\n"
        "• Posez une question éducative (Gemini)\n"
        "• /test → Test de niveau de langue"
    )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO users (telegram_id, score, question_index) VALUES (?,0,0)",
        (user_id,)
    )
    conn.commit()
    conn.close()

    q_data = get_question(0)
    if not q_data:
        await update.message.reply_text("❌ Aucune question disponible.")
        return

    (qid, question), choices = q_data

    keyboard = [
        [InlineKeyboardButton(text=c[1], callback_data=str(c[0]))]
        for c in choices
    ]

    await update.message.reply_text(
        f"📝 Test de niveau\n\n{question}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def qcm_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choix_id = int(query.data)
    user_id = query.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT correct FROM choices WHERE id=?", (choix_id,))
    correct = cursor.fetchone()[0]

    cursor.execute(
        "SELECT score, question_index FROM users WHERE telegram_id=?",
        (user_id,)
    )
    score, index = cursor.fetchone()

    if correct:
        score += 1

    index += 1

    cursor.execute(
        "UPDATE users SET score=?, question_index=? WHERE telegram_id=?",
        (score, index, user_id)
    )
    conn.commit()
    conn.close()

    q_data = get_question(index)
    if not q_data:
        niveau = estimer_niveau(score)
        await query.edit_message_text(
            f"🎓 Test terminé !\n\n"
            f"Score : {score}\n"
            f"Niveau estimé : {niveau}"
        )
        return

    (qid, question), choices = q_data
    keyboard = [
        [InlineKeyboardButton(text=c[1], callback_data=str(c[0]))]
        for c in choices
    ]

    await query.edit_message_text(
        f"{question}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text
    reply = ask_gemini(user_id, user_text)
    await update.message.reply_text(reply)

# ===========================
# MAIN
# ===========================

def main():
    init_db()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CallbackQueryHandler(qcm_answer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main() 

