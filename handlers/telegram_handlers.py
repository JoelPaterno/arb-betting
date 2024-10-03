# Handlers for the Telegram bot commands
from telegram import Update
from telegram.ext import CallbackContext
from db.db import SessionLocal
from db.models import ArbitrageOpportunity

def search_arbitrage(update: Update, context: CallbackContext):
    session = SessionLocal()
    opportunities = session.query(ArbitrageOpportunity).all()

    if not opportunities:
        update.message.reply_text("No arbitrage opportunities found.")
    else:
        message = ""
        for opportunity in opportunities:
            message += f"Match: {opportunity.match}\n"
            message += f"Bookmakers: {opportunity.bookmaker1} vs {opportunity.bookmaker2}\n"
            message += f"Profit: {opportunity.profit}%\n\n"

        update.message.reply_text(message)

    session.close()