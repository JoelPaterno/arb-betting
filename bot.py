# Main script to run the Telegram bot
from telegram.ext import Updater, CommandHandler
from handlers.telegram_handlers import search_arbitrage

def main():
    updater = Updater("BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Add command handler for searching arbitrage opportunities
    dp.add_handler(CommandHandler("search", search_arbitrage))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
