import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ApplicationBuilder
from telegram.error import TelegramError, Conflict

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7793247780:AAHGFMUp1O-h36VoXyMJaN4LBhToPyONREI")
WEB_APP_URL = "https://darling-arithmetic-c95178.netlify.app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    try:
        user_name = update.message.from_user.first_name  # Get user's first name
        # Create the inline button
        button = InlineKeyboardButton("Click Me To See", web_app={"url": WEB_APP_URL})
        keyboard = InlineKeyboardMarkup([[button]])

        # Send a personalized greeting message with an inline button
        await update.message.reply_text(
            f"Hello {user_name}!\nWelcome to FamXExclusive Bot!\nTap the button below to see our offers!",
            reply_markup=keyboard
        )
        logger.info(f"Sent welcome message to chat ID: {update.effective_chat.id}")

    except TelegramError as te:
        logger.error(f"Telegram API error in start command: {te}")
    except Exception as e:
        logger.error(f"Unexpected error in start command: {e}", exc_info=True)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors caused by updates."""
    try:
        logger.error(f"Update {update} caused error: {context.error}", exc_info=True)

        if isinstance(context.error, Conflict):
            logger.error("Conflict error: Multiple bot instances detected. Stopping bot...")
            await context.application.stop()
            logger.info("Bot stopped. Please ensure only one instance is running.")

    except Exception as e:
        logger.error(f"Error in error_handler: {e}", exc_info=True)

def main():
    """Run the bot with polling."""
    try:
        bot_token = BOT_TOKEN
        if not bot_token:
            raise ValueError("BOT_TOKEN not set")

        # Create the bot application
        application = Application.builder().token(bot_token).build()

        # Add the /start command handler
        application.add_handler(CommandHandler("start", start))
        # Add error handler
        application.add_error_handler(error_handler)

        # Start polling for updates
        logger.info("Starting bot with polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
