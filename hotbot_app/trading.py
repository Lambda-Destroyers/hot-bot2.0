import requests
import time
import hmac
import hashlib
import base64
import json
import pandas as pd

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
