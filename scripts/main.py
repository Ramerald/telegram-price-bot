import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Fetch the Telegram bot token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable not set")

# URL to fetch Bitcoin price from CoinGecko
BITCOIN_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

def get_bitcoin_price():
    try:
        response = requests.get(BITCOIN_PRICE_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("bitcoin", {}).get("usd", "Unavailable")
    except Exception as e:
        return f"Error: {e}"

def price(update: Update, context: CallbackContext):
    price_usd = get_bitcoin_price()
    update.message.reply_text(f"Current Bitcoin price: ${price_usd}")

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handler for /price
    dispatcher.add_handler(CommandHandler("price", price))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
