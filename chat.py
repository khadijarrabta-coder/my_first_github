import logging
import requests
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------------------
# CONFIGURATION
# ---------------------------
GEMINI_API_KEYS = [
    "AIzaSyD_dM5ja0CESUCPoDJyUN3jxxzfGEzVaHc",
    "AIzaSyBdkIc7rwc5VyJ07DSXerSLPf4Mt7B3R7I",
    "AIzaSyB1bN3L6hCpHGdry_0Ub4iRfdJ1kKbhqE4"
]

GEMINI_MODEL = "gemini-2.5-flash"
TELEGRAM_BOT_TOKEN = "8537081885:AAEmpmMTfz8CZptBVsXSQuB5UV82Rjl89v4"

# Prompt éducatif
EDUCATIONAL_PROMPT = """
Tu es un professeur pour des étudiants.
Réponds uniquement aux questions éducatives sur les matières suivantes : Mathématiques, Sciences, Langues.
- Pour Maths et Sciences : explique normalement.
- Pour les questions de langues (traduction de mots ou grammaire) : donne la traduction ou l'explication.
Ne réponds pas aux questions hors sujet.
Si la question n’est pas dans ces matières, répond :
"Je ne réponds qu’aux questions sur les matières scolaires (Maths, Sciences, Langues)."
"""

MAX_RETRIES = 2

# ---------------------------
# LOGGER
# ---------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------------------
# MÉMOIRE DES CONVERSATIONS PAR UTILISATEUR
# ---------------------------
conversation_history = {}

# ---------------------------
# FONCTION PRINCIPALE : APPEL GEMINI
# ---------------------------
def ask_gemini(user_id, user_message):
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append(f"Étudiant: {user_message}")
    full_prompt = EDUCATIONAL_PROMPT + "\n" + "\n".join(conversation_history[user_id]) + "\nProfesseur:"

    for attempt in range(MAX_RETRIES):
        for api_key in GEMINI_API_KEYS:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
            payload = {"contents":[{"parts":[{"text":full_prompt}]}]}

            try:
                response = requests.post(api_url, json=payload, timeout=10)

                if response.status_code == 200:
                    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    conversation_history[user_id].append(f"Professeur: {reply}")
                    return reply

                if response.status_code in [403, 429]:
                    logger.warning("Quota atteint pour cette clé, passage à la suivante...")
                    continue

                if response.status_code == 503:
                    logger.warning("Modèle surchargé, attente 1s puis retentative...")
                    time.sleep(1)
                    continue

                logger.error(f"Erreur Gemini {response.status_code}: {response.text}")

            except Exception as e:
                logger.error(f"Erreur réseau : {e}")

        time.sleep(1)

    return "🤖 Je rencontre un petit souci, réessayons dans quelques secondes..."

# ---------------------------
# HANDLERS TELEGRAM
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bonjour ! Posez-moi une question sur Maths, Sciences ou Langues et je vous répondrai. Pour les langues, précisez que vous voulez une traduction ou grammaire."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"Message reçu de {user_id} : {user_text}")

    reply = ask_gemini(user_id, user_text)
    await update.message.reply_text(reply)

# ---------------------------
# MAIN
# ---------------------------
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()


