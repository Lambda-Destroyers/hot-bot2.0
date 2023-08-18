import pytest
from unittest.mock import patch, Mock
from sandbox_module import retrieve, process, training, main_script
import pandas


# Test for retrieve.py
def test_create_headers():
    method = "GET"
    request_path = "/accounts"
    body = ""
    headers = retrieve.create_headers(method, request_path, body)

    # Check that the required headers are present
    assert 'CB-ACCESS-KEY' in headers
    assert 'CB-ACCESS-SIGN' in headers
    assert 'CB-ACCESS-TIMESTAMP' in headers
    assert 'CB-ACCESS-PASSPHRASE' in headers
    assert 'Content-Type' in headers

def test_get_product_id():
    base_currency = "BTC"
    quote_currency = "USD"
    product_id = retrieve.get_product_id(base_currency, quote_currency)
    assert product_id == "BTC-USD"

# Test for process.py
def test_process_historical_data():
    data = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]
    processed_data = process.process_historical_data(data)
    assert list(processed_data) == [4, 10]

# Test for training.py
def test_predict_future_price():
    historical_data = [1, 2, 3, 4, 5]
    future_price = training.predict_future_price(historical_data)
    assert future_price > historical_data[-1]

# Test for main_script.py
def test_calculate_roi():
    mock_response = {
        'price': '100',
        'executed_value': '120'
    }
    roi = main_script.calculate_roi(mock_response)
    assert roi == 20.0

@patch('requests.post')
def test_create_order(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {
        'id': 'd0c5340b-6d6c-49d9-b567-48c4bfca13d9',
        'product_id': 'BTC-USD',
        'side': 'buy',
        'type': 'limit',
        'size': '0.001',
        'price': '100.00'
    }
    mock_post.return_value = mock_response

    response = main_script.create_order('BTC-USD', 'buy', 'limit', size='0.001', price='100.00')
    assert response['id'] == 'd0c5340b-6d6c-49d9-b567-48c4bfca13d9'

# Note: The following tests require a network connection and a valid API configuration.

# @pytest.mark.skip(reason="Network-dependent test")
def test_get_account_info():
    account_info = retrieve.get_account_info()
    assert "message" not in account_info

# @pytest.mark.skip(reason="Network-dependent test")
def test_fetch_historical_data():
    product_id = "BTC-USD"
    granularity = 3600
    historical_data = retrieve.fetch_historical_data(product_id, granularity)
    assert isinstance(historical_data, list)
    assert len(historical_data) > 0
