import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)
from telegram.error import TelegramError, Conflict

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token and web URL
BOT_TOKEN = "7793247780:AAHGFMUp1O-h36VoXyMJaN4LBhToPyONREI"
WEB_APP_URL = "https://darling-arithmetic-c95178.netlify.app/"

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_name = update.message.from_user.first_name
        chat_type = update.effective_chat.type
        logger.info(f"/start from {user_name} in {chat_type}")

        button = InlineKeyboardButton("Click Me To See", web_app={"url": WEB_APP_URL})
        keyboard = InlineKeyboardMarkup([[button]])

        await update.message.reply_text(
            f"Hello {user_name}!\nWelcome to FamXExclusive Bot!\nTap the button below to see our offers!",
            reply_markup=keyboard
        )

    except TelegramError as te:
        logger.error(f"Telegram API error: {te}")
    except Exception as e:
        logger.error(f"Unexpected error in /start: {e}", exc_info=True)

# Fallback debug handler — echoes any message
async def echo_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        chat_type = update.effective_chat.type
        message = update.message.text
        logger.info(f"Message from {user.username or user.first_name} in {chat_type}: {message}")
        await update.message.reply_text("I see your message!")
    except Exception as e:
        logger.error(f"Error in echo_all: {e}", exc_info=True)

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.error(f"Update error: {context.error}", exc_info=True)
        if isinstance(context.error, Conflict):
            logger.error("Conflict detected — stopping bot.")
            await context.application.stop()
    except Exception as e:
        logger.error(f"Error in error handler: {e}", exc_info=True)

# Main function
def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.ALL, echo_all))
        application.add_error_handler(error_handler)

        logger.info("Bot is starting...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
