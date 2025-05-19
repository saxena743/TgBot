import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
from telegram.error import TelegramError, Conflict

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "7793247780:AAHGFMUp1O-h36VoXyMJaN4LBhToPyONREI"
WEB_APP_URL = "https://darling-arithmetic-c95178.netlify.app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command in private and group chats."""
    try:
        chat_type = update.effective_chat.type
        user_name = update.message.from_user.first_name
        logger.info(f"/start command received from {user_name} in chat type: {chat_type}")

        # Create inline keyboard
        button = InlineKeyboardButton("Click Me To See", web_app={"url": WEB_APP_URL})
        keyboard = InlineKeyboardMarkup([[button]])

        # Send message
        await update.message.reply_text(
            f"Hello {user_name}!\nWelcome to FamXExclusive Bot!\nTap the button below to see our offers!",
            reply_markup=keyboard
        )

    except TelegramError as te:
        logger.error(f"Telegram API error in start command: {te}")
    except Exception as e:
        logger.error(f"Unexpected error in start command: {e}", exc_info=True)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log all errors."""
    try:
        logger.error(f"Update caused error: {context.error}", exc_info=True)
        if isinstance(context.error, Conflict):
            logger.error("Conflict error: Multiple bot instances detected. Stopping bot...")
            await context.application.stop()
    except Exception as e:
        logger.error(f"Error in error_handler: {e}", exc_info=True)

def main():
    """Run the bot using polling."""
    try:
        bot_token = BOT_TOKEN
        if not bot_token:
            raise ValueError("BOT_TOKEN not set")

        # Create application
        application = Application.builder().token(bot_token).build()

        # Add command handler
        application.add_handler(CommandHandler("start", start))
        application.add_error_handler(error_handler)

        # Start polling
        logger.info("Starting bot with polling...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
