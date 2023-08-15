import requests

COINBASE_API_URL = "https://api-public.sandbox.exchange.coinbase.com/"
API_KEY = "60fc27c1b7540cd1f99be2cf81fb010a"  # Replace with your actual API key

def get_product_id(base_currency, quote_currency):
    return f"{base_currency}-{quote_currency}"

def create_order(product_id, side, order_type, size=None, funds=None, price=None):
    headers = {
        "Authorization": f"Bearer {API_KEY}"  # Include your API key in the Authorization header
    }

    order_data = {
        "product_id": product_id,
        "side": side,
        "type": order_type,
        "size": size,
        "funds": funds,
        "price": price
    }
    response = requests.post(f"{COINBASE_API_URL}orders", json=order_data, headers=headers)
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

# Example usage
amount_to_trade = 0.001
base_currency = "BTC"
quote_currency = "USD"
side = "buy"  # "buy" or "sell"
order_type = "limit"  # "limit" or "market"
price = 10000  # Specify a price for limit orders, None for market orders

response = trade_crypto(base_currency, quote_currency, amount_to_trade, side, order_type, price)
print("Trade response:", response)