import pandas as pd
import json

def process_historical_data(data):
    data = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    return data['close']
