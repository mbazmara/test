from fbprophet import Prophet
import pandas as pd


def predict_the_stock(data):
    df_rain = data[['Date', 'Close']]
    df_rain = df_rain.rename(columns={"Date": "ds", "Close": "y"})
    m = Prophet()
    m.fit(df_rain)
    future = m.make_future_dataframe(periods=40)
    forecast = m.predict(future)
    return m, forecast
