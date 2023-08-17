import requests
import time
import hmac
import hashlib
import base64
import json

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

def fetch_historical_data(product_id, granularity):
    method = 'GET'
    request_path = f'/products/{product_id}/candles?granularity={granularity}'
    headers = create_headers(method, request_path)
    response = requests.get(f"{COINBASE_API_URL}products/{product_id}/candles?granularity={granularity}", headers=headers)
    return response.json()
