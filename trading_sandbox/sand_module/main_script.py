import retrieve
import process
import training
import time
import pandas as pd
import json
import requests

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
    if price and order_type == "limit": # Only include the price parameter if the order type is "limit"
        body["price"] = str(price)
        print(f"Price: {price}")
    body_str = json.dumps(body, separators=(',', ':'))
    headers = retrieve.create_headers(method, request_path, body_str)

    response = requests.post(f"{retrieve.COINBASE_API_URL}orders", data=body_str, headers=headers)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response.")
        return None

    if "message" in response_json:
        print(f"Error: {response_json['message']}")
        return None
    else:
        response_json.pop('message', None)
        return response_json

def trade_crypto(base_currency, quote_currency, amount, side, order_type, price=None, retry_attempts=10, price_adjustment=0.05):
    product_id = retrieve.get_product_id(base_currency, quote_currency)
    historical_data = retrieve.fetch_historical_data(product_id, 3600)  # Example granularity
    processed_data = process.process_historical_data(historical_data)
    predicted_price = training.predict_future_price(processed_data)
    if predicted_price > processed_data.iloc[-1]:
        side = "buy"
    else:
        side = "sell"

    attempts = 0
    while attempts < retry_attempts:
        adjusted_price = round(predicted_price * (1 + price_adjustment * attempts), 2)
        order_configuration = {
            "size": str(amount),
            "price": str(adjusted_price),  # Use the adjusted price in the order
        }
        print(f"Adjusted Price: {adjusted_price}")
        response = create_order(product_id, side, order_type, **order_configuration)
        if response is None or "message" in response:
            # Print the error message received
            if response:
                print(f"Error message received: {response['message']}")
            
            # Always increment attempts and adjust price, regardless of error message
            attempts += 1
            continue
        else:
            return response  # Return the successful response

    # Return None if all retry attempts failed
    return None


def print_trade_response_as_table(response):
    if response:
        df = pd.DataFrame(list(response.items()), columns=["Key", "Value"])
        print(df)
    else:
        print("Error: No response received.")


def calculate_roi(initial_price, final_price):
    if initial_price is None or final_price is None:
        return None
    return ((final_price - initial_price) / initial_price) * 100

def calculate_roi(response):
    if response is None or 'price' not in response or 'executed_value' not in response:
        print("Error: No response received for ROI calculation.")
        return None

    initial_price = float(response['price'])
    final_price = float(response['executed_value'])
    return ((final_price - initial_price) / initial_price) * 100



if __name__ == "__main__":
    max_trades = 5
    trade_count = 0
    base_currency = "BTC"
    quote_currency = "USD"
    amount_to_trade = 0.1
    order_type = "market"

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
            roi = calculate_roi(response)
            if roi is not None:
                print(f"ROI: {roi:.2f}%")

            trade_count += 1
        except Exception as e:
            print(f"Error: {e}")
