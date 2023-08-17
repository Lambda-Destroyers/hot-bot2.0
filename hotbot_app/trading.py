import requests
import time
import hmac
import hashlib
import base64
import json
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import config as CONFIG

API_KEY = '60fc27c1b7540cd1f99be2cf81fb010a'
API_SECRET = 'Vb54QDcZxH8ecWHKBJI7d85AjMHzwFplWMK/k6YPEolLrrwk2gkIYgZkf7LF0mS7LtznH7jDu/hVQy9LYWdtAA=='
API_PASSPHRASE = 'mm07qohm8q'
COINBASE_API_URL = "https://api-public.sandbox.exchange.coinbase.com/"

def create_headers(method, request_path, body=''):
    timestamp = str(int(time.time()))
    signature_data = f'{timestamp}{method}{request_path}{body}'.encode('ascii')
    signature = hmac.new(base64.b64decode(API_SECRET), signature_data, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

    headers = {
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': API_PASSPHRASE,
        'Content-Type': 'application/json'
    }
    return headers

def get_account_info():
    method = 'GET'
    request_path = '/accounts'
    headers = create_headers(method, request_path)
    response = requests.get(f"{COINBASE_API_URL}accounts", headers=headers)
    return response.json()

def get_product_id(base_currency, quote_currency):
    return f"{base_currency}-{quote_currency}"

def create_order(product_id, side, order_type, size=None, funds=None, price=None):
    method = 'POST'
    request_path = '/orders'
    body = {
        "product_id": product_id,
        "side": side,
        "type": order_type
    }
    if size:
        body["size"] = str(size)
    if funds:
        body["funds"] = str(funds)
    if price:
        body["price"] = str(price)
        print(f"Price: {price}")
    else:
        body.pop("price", None)
    body_str = json.dumps(body, separators=(',', ':'))
    headers = create_headers(method, request_path, body_str)

    response = requests.post(f"{COINBASE_API_URL}orders", data=body_str, headers=headers)
    return response.json()

def fetch_historical_data(product_id):
    method = 'GET'
    request_path = f'/products/{product_id}/candles?granularity=3600'
    headers = create_headers(method, request_path)
    response = requests.get(f"{COINBASE_API_URL}products/{product_id}/candles?granularity=3600", headers=headers)
    data = pd.DataFrame(response.json(), columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    return data['close']

def predict_future_price(historical_data):
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = historical_data
    model = LinearRegression()
    model.fit(X, y)
    future_price = model.predict(np.array([[len(historical_data)]]))
    return future_price[0]

def trade_crypto(base_currency, quote_currency, amount, side, order_type, price=None):
    product_id = get_product_id(base_currency, quote_currency)
    historical_data = fetch_historical_data(product_id)
    predicted_price = predict_future_price(historical_data)
    price = round(predicted_price, 2) # Set the price based on the predicted price
    if predicted_price > historical_data.iloc[-1]:
        side = "buy"
    else:
        side = "sell"
    order_configuration = {
        "size": str(amount),
        "price": str(price),
    }
    response = create_order(product_id, side, order_type, **order_configuration)
    return response


def print_trade_response_as_table(response):
    df = pd.DataFrame(list(response.items()), columns=["Key", "Value"])
    print(df)

def calculate_roi(initial_price, final_price):
    return ((final_price - initial_price) / initial_price) * 100

max_trades = 5
trade_count = 0
base_currency = "BTC"
quote_currency = "USD"
amount_to_trade = 0.001
order_type = "limit"

while trade_count < max_trades:
    try:
        # Execute a trade
        response = trade_crypto(base_currency, quote_currency, amount_to_trade, "buy", order_type)
        print_trade_response_as_table(response)

        # Wait for a certain time (e.g., 60 seconds)
        time.sleep(5)

        # Execute another trade
        response = trade_crypto(base_currency, quote_currency, amount_to_trade, "sell", order_type)
        print_trade_response_as_table(response)

        # Calculate and print ROI
        roi = calculate_roi(response['price'], response['executed_value'])
        print(f"ROI: {roi:.2f}%")

        trade_count += 1
    except Exception as e:
        print(f"Error: {e}")
import requests
import time
import hmac
import hashlib
import base64
import json
import pandas as pd
from config import CONFIG

API_KEY = CONFIG["API_KEY"]
print(API_KEY)
API_SECRET= CONFIG["API_SECRET"]
API_PASSPHRASE = CONFIG["API_PASSPHRASE"]
COINBASE_API_URL = CONFIG["COINBASE_API_URL"]


def create_headers(method, request_path, body=''):
    timestamp = str(int(time.time()))
    signature_data = f'{timestamp}{method}{request_path}{body}'.encode('ascii')
    signature = hmac.new(base64.b64decode(API_SECRET), signature_data, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

    headers = {
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': API_PASSPHRASE,
        'Content-Type': 'application/json'
    }
    return headers

def get_account_info():
    method = 'GET'
    request_path = '/accounts'
    headers = create_headers(method, request_path)
    response = requests.get(f"{COINBASE_API_URL}accounts", headers=headers)
    print(f"HTTP Status Code: {response.status_code}")

    return response.json()

def get_product_id(base_currency, quote_currency):
    return f"{base_currency}-{quote_currency}"

def create_order(product_id, side, order_type, size=None, funds=None, price=None):
    method = 'POST'
    request_path = '/orders'
    body = {
        "product_id": product_id,
        "side": side,
        "type": order_type,
        "size": str(size) if size else None,
        "funds": str(funds) if funds else None,
        "price": str(price) if price else None
    }
    body_str = json.dumps(body, separators=(',', ':'))
    headers = create_headers(method, request_path, body_str)

    response = requests.post(f"{COINBASE_API_URL}orders", data=body_str, headers=headers)
    print(f"HTTP Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    return response.json()
   
def trade_crypto(base_currency, quote_currency, amount, side, order_type, price=None):
    product_id = get_product_id(base_currency, quote_currency)

    if order_type == "limit":
        order_configuration = {
            "size": str(amount),
            "price": str(price),
        }
    else:
        order_configuration = {
            "size": str(amount),
        }

    response = create_order(product_id, side, order_type, **order_configuration)
    return response

def print_trade_response_as_table(response):
    df = pd.DataFrame(list(response.items()), columns=["Key", "Value"])
    print(df)

def print_account_info_as_table(account_info):
    # Filter out assets with zero balance
    non_zero_assets = [{'Currency': asset['currency'], 'Balance': asset['balance']} for asset in account_info if float(asset['balance']) > 0]

    # Convert the filtered list of assets into a DataFrame and print it
    df = pd.DataFrame(non_zero_assets)
    print(df)



# Example usage
amount_to_trade = 0.001
base_currency = "BTC"
quote_currency = "USD"
side = "buy"  # "buy" or "sell"
order_type = "limit"  # "limit" or "market"
price = 10000  # Specify a price for limit orders, None for market orders

# Execute a trade
response = trade_crypto(base_currency, quote_currency, amount_to_trade, side, order_type, price)
print_trade_response_as_table(response)

# Fetch and print account information
account_info = get_account_info()
print_account_info_as_table(account_info)
