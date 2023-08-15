# modules/gpt_controller.py

import requests
import json
import datetime
import matplotlib.pyplot as plt
from modules.investment_recommendation import get_investment_recommendation
from modules.historical_getter import get_historical_data
from modules.current_price import get_current_price
from modules.option import user_option
import time
import logging

from rich.console import Console

console = Console()

# Load API keys from files
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

with open('gpt_api.txt', 'r') as file:
    gpt_api = file.read().strip()

# Set headers for API requests
headers = {
    "CB-ACCESS-KEY": api_key,
}

# Create a logger
logger = logging.getLogger('crypto_bot')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('crypto_bot.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_prices(days, option):
    btc_usd_price = get_current_price("BTC-USD", headers)
    eth_usd_price = get_current_price("ETH-USD", headers)

    api_url = "https://api.pro.coinbase.com/products"

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(int(days))

    btc_data = get_historical_data("BTC-USD", api_url, start_date, end_date)
    btc_timestamps = [datetime.datetime.fromtimestamp(int(entry[0])) for entry in btc_data]
    btc_opens = [entry[3] for entry in btc_data]
    btc_highs = [entry[2] for entry in btc_data]
    btc_lows = [entry[1] for entry in btc_data]
    btc_closes = [entry[4] for entry in btc_data]

    eth_data = get_historical_data("ETH-USD", api_url, start_date, end_date)
    eth_timestamps = [datetime.datetime.fromtimestamp(int(entry[0])) for entry in eth_data]
    eth_opens = [entry[3] for entry in eth_data]
    eth_highs = [entry[2] for entry in eth_data]
    eth_lows = [entry[1] for entry in eth_data]
    eth_closes = [entry[4] for entry in eth_data]

    user_option(btc_data, eth_data, btc_opens, btc_highs, btc_lows, btc_closes, eth_opens, eth_highs, eth_lows, eth_closes, gpt_api, days, option)
    show_plot(btc_timestamps, btc_closes, btc_lows, btc_highs, eth_timestamps, eth_closes, eth_lows, eth_highs, days)

def show_plot(btc_timestamps, btc_closes, btc_lows, btc_highs, eth_timestamps, eth_closes, eth_lows, eth_highs, days):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(btc_timestamps, btc_closes, color='blue')
    ax1.vlines(btc_timestamps, btc_lows, btc_highs, color='black', linewidth=1)
    ax1.set_title(f"Bitcoin (BTC-USD) - {days} Day Historical Data")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price (USD)")
    ax2.plot(eth_timestamps, eth_closes, color='green')
    ax2.vlines(eth_timestamps, eth_lows, eth_highs, color='black', linewidth=1)
    ax2.set_title(f"Ethereum (ETH-USD) - {days} Day Historical Data")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price (USD)")
    fig.autofmt_xdate()  
    plt.tight_layout()
    plt.show()

def get_option(days, option):
    get_prices(days, option)

def perform_trades(api, symbol, investment_amount):
    while True:
        btc_usd_price = get_current_price("BTC-USD", headers)
        eth_usd_price = get_current_price("ETH-USD", headers)

        roi_btc = ((btc_usd_price - investment_amount) / investment_amount) * 100
        roi_eth = ((eth_usd_price - investment_amount) / investment_amount) * 100

        # Log bot actions with different log levels
        logger.info("Checking and performing trades...")

        if roi_btc >= 5:
            api.execute_order(symbol, 'buy', quantity=0.1, price=btc_usd_price)
            logger.info("Buying BTC due to ROI increase.")
        elif roi_btc <= -2:
            api.execute_order(symbol, 'sell', quantity=0.1, price=btc_usd_price)
            logger.warning("Selling BTC due to significant ROI decrease.")
        else:
            logger.debug("No action taken for BTC.")

        if roi_eth >= 5:
            api.execute_order(symbol, 'buy', quantity=0.1, price=eth_usd_price)
            logger.info("Buying ETH due to ROI increase.")
        elif roi_eth <= -2:
            api.execute_order(symbol, 'sell', quantity=0.1, price=eth_usd_price)
            logger.warning("Selling ETH due to significant ROI decrease.")
        else:
            logger.debug("No action taken for ETH.")

        time.sleep(60)  # Wait for 1 minute before checking again


# Add any remaining functions and code
