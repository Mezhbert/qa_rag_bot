import logging
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, 
                          MessageHandler, ContextTypes, filters)

import os
from app.constants import START_MSG
from app.retriever import get_standard_qa_chain

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN не задан в окружении")
    exit(1)

qa_chain = get_standard_qa_chain()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MSG)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    logging.info(f"[Bot] Question received: {msg}")

    if not msg:
        await update.message.reply_text("Please enter a question.")
        return

    try:
        logging.info("[Bot] Searching for an answer...")
        response = qa_chain.invoke({"query": msg})
        answer = response.get('result') or "No information on this question in the standard."
        logging.info(f"[Bot] Answer: {answer}")
        await update.message.reply_text(answer)

    except Exception as e:
        logging.exception(f"[Bot] Error processing query: {e}")
        await update.message.reply_text("Error processing your request.")

def run():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    logging.info("Запуск Telegram бота...")
    app.run_polling()

if __name__ == "__main__":
    run()
