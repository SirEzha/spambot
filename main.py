import os
import logging
import asyncio
import aiofiles
from datetime import datetime
from telegram import Update, MessageEntity
from telegram.ext import (
    ApplicationBuilder, MessageHandler, filters, ContextTypes
)
from ollama_check import is_spam_with_ollama
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("CHAT_ID")

async def log_message_async(message_text: str, username: str, date: datetime, verdict: str):
    """
    Safely log message details to CSV file asynchronously
    """
    try:
        # Sanitize data for CSV safety
        safe_text = message_text.replace('"', '""')[:500]  # Limit length and escape quotes
        safe_username = username.replace('"', '""')[:100]
        
        log_entry = [safe_text, safe_username, date.isoformat(), verdict]
        
        # Use proper CSV writing with async file operations
        async with aiofiles.open('message_log.csv', 'a', encoding='utf-8', newline='') as f:
            # For async CSV writing, we'll format manually but safely
            csv_line = ','.join(f'"{field}"' for field in log_entry) + '\n'
            await f.write(csv_line)
            
    except Exception as e:
        logging.error(f"Error logging message: {e}")

# Handler for all messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    username = message.from_user.username

    # Ignore messages outside the target chat
    if message.chat.id != TARGET_CHAT_ID:
        return

    # Skip attachments (non-text messages)
    if not message.text:
        return

    verdict = "Not Spam"
    # try:
    #     spam = await is_spam_with_ollama(message.text)
    #     if spam:
    #         verdict = "Spam"
    #         pass
    #         # await message.delete()
    # except Exception as e:
    #     logging.error(f"Error while checking spam: {e}")
    #     verdict = "Error"

    await log_message_async(message.text, username, message.date, verdict)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, message_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
