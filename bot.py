from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Your bot token
BOT_TOKEN = "7547766289:AAFNJ1PLTxAgU_skkTcPFtbQLZEzHdwHOHA"

# Your Netlify website URL
WEB_APP_URL = "https://darling-youtiao-320512.netlify.app/" 


# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # Get user's first name
    # Create the inline button
    button = InlineKeyboardButton("Click Me To See", web_app={"url": WEB_APP_URL})
    keyboard = InlineKeyboardMarkup([[button]])
    
    # Send a personalized greeting message with an inline button
    await update.message.reply_text(
        f"Hello {user_name}!\nWelcome to FamXExclusive Bot!\nTap the button below to see our offers!",
        reply_markup=keyboard
    )

# Main function to run the bot
def main():
    # Create the bot application (replacing Updater)
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))
    
    # Start polling for updates
    application.run_polling()

if __name__ == "__main__":
    main()
