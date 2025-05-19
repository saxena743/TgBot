import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ApplicationBuilder
from telegram.error import TelegramError, Conflict, Forbidden

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7793247780:AAHGFMUp1O-h36VoXyMJaN4LBhToPyONREI")
WEB_APP_URL = "https://darling-arithmetic-c95178.netlify.app/"

# Plans data (synced with website)
plans = [
    {"title": "FamXCreeps", "price": "₹499 Lifetime"},
    {"title": "FamXElite", "price": "₹199/Month"},
    {"title": "FamXSpy", "price": "₹199/Month"},
    {"title": "FamXInc3st VIP", "price": "₹1999 Permanent"},
    {"title": "All in One", "price": "₹7000 Permanent"},
    {"title": "Numbers For OTP", "price": "Varies by Country"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with a personalized greeting and inline button."""
    try:
        if not update.message or not update.effective_chat:
            logger.error("Invalid update: No message or chat found")
            return

        user_name = update.message.from_user.first_name or "User"
        button = InlineKeyboardButton("View Offers", web_app={"url": WEB_APP_URL})
        keyboard = InlineKeyboardMarkup([[button]])

        welcome_message = (
            f"Hello {user_name}!\n"
            "Welcome to FamXExclusive Bot! 🎉\n"
            "Tap the button below to see our subscription plans!"
        )

        await update.message.reply_text(welcome_message, reply_markup=keyboard)
        logger.info(f"Sent welcome message to chat ID: {update.effective_chat.id}")

    except Forbidden as fe:
        logger.warning(f"Cannot send message to chat ID {update.effective_chat.id}: {fe}")
    except TelegramError as te:
        logger.error(f"Telegram API error in start command: {te}")
    except Exception as e:
        logger.error(f"Unexpected error in start command: {e}", exc_info=True)

async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List available subscription plans."""
    try:
        if not update.message or not update.effective_chat:
            logger.error("Invalid update: No message or chat found")
            return

        plans_list = "\n".join(f"- {plan['title']}: {plan['price']}" for plan in plans)
        message = (
            f"Available Plans:\n{plans_list}\n"
            "Join us at https://t.me/RealButcherFam or visit our website!"
        )
        button = InlineKeyboardButton("View on Website", web_app={"url": WEB_APP_URL})
        keyboard = InlineKeyboardMarkup([[button]])

        await update.message.reply_text(message, reply_markup=keyboard)
        logger.info(f"Sent plans to chat ID: {update.effective_chat.id}")

    except Forbidden as fe:
        logger.warning(f"Cannot send plans to chat ID {update.effective_chat.id}: {fe}")
    except TelegramError as te:
        logger.error(f"Telegram API error in plans command: {te}")
    except Exception as e:
        logger.error(f"Unexpected error in plans command: {e}", exc_info=True)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors caused by updates."""
    try:
        logger.error(f"Update {update} caused error: {context.error}", exc_info=True)

        if isinstance(context.error, Conflict):
            logger.error("Conflict error: Multiple bot instances detected. Stopping bot...")
            await context.application.stop()
            logger.info("Bot stopped. Please ensure only one instance is running.")
        elif isinstance(context.error, Forbidden):
            logger.warning(f"Blocked by user: {context.error}")
            admin_chat_id = os.getenv("ADMIN_CHAT_ID")
            if admin_chat_id and update and update.effective_chat:
                try:
                    await context.bot.send_message(
                        chat_id=admin_chat_id,
                        text=f"Bot was blocked by user in chat ID: {update.effective_chat.id}"
                    )
                except TelegramError as admin_error:
                    logger.error(f"Failed to notify admin: {admin_error}")
        else:
            if update and update.effective_message:
                try:
                    await update.effective_message.reply_text(
                        "An error occurred. Please try again later or contact support."
                    )
                except Forbidden:
                    logger.warning("Cannot notify user: Bot is blocked")
                except TelegramError as te:
                    logger.error(f"Failed to notify user: {te}")

    except Exception as e:
        logger.error(f"Error in error_handler: {e}", exc_info=True)

def main() -> None:
    """Run the bot."""
    try:
        bot_token = BOT_TOKEN
        if not bot_token:
            raise ValueError("BOT_TOKEN not set")

        application = ApplicationBuilder().token(bot_token).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("plans", plans))
        application.add_error_handler(error_handler)

        logger.info("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
