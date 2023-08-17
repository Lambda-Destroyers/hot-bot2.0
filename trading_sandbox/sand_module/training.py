from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future_price(historical_data):
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = historical_data
    model = LinearRegression()
    model.fit(X, y)
    future_price = model.predict(np.array([[len(historical_data)]]))
    return future_price[0]


