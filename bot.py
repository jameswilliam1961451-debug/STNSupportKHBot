import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging for Render console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Your updated Khmer welcome message
    welcome_text = (
        "សួស្តី 👋\n"
        "សូមស្វាគមន៍មកកាន់ STN Help Center។\n\n"
        "សូមជ្រើសរើសម៉ឺនុយខាងក្រោម ដើម្បីទទួលព័ត៌មាន ឬស្នើសុំជំនួយ។\n"
        "បើមានបញ្ហាបន្ទាន់ សូមពិពណ៌នាបញ្ហារបស់អ្នក ហើយយើងនឹងឆ្លើយតបឲ្យបានឆាប់តាមដែលអាចធ្វើបាន។"
    )
    await update.message.reply_text(welcome_text)

async def main():
    # Retrieve the token from Render Environment Variables
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("FATAL: TELEGRAM_TOKEN not found in Environment Variables!")
        return

    # Initialize the Application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Register the /start command
    application.add_handler(CommandHandler("start", start))
    
    logger.info("--- STN HELP CENTER BOT STARTING ---")
    
    # Modern startup sequence for Python 3.14+
    async with application:
        await application.initialize()
        await application.start()
        # drop_pending_updates=True ignores messages sent while the bot was offline
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Keep the background worker alive indefinitely
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        # This is the correct way to launch the loop in Python 3.14
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by system.")
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}")
