import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import plot_data as pt
from prediction_model import predict_the_stock
from fbprophet.plot import plot_plotly

# ---- website config ----
st.set_page_config  (page_title='Stock', page_icon=':chart_with_upwards_trend:')
# create a dataframe of symbols
symbols_list = pd.read_csv('All_Symbols.csv')
st.title('Welcome to our stock forcast')
st.subheader('Pick a symbol of stock you want to predict:')
left, middle, right = st.columns(3)
with left:
    Company = st.selectbox(label='symbols', options=symbols_list['Symbol'].unique())
with middle:
    start = st.date_input("Pick a start date", datetime.date(2022, 1, 1))
with right:
    s = date.today().strftime("%Y-%m-%d")
    end = st.date_input("Pick an end date")
n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365
load_inputs = st.button(label='Loading Data')

if load_inputs:
    loading_text = st.text("Data is loading...")
    tickerSymbol = Company
    tickerData = yf.Ticker(tickerSymbol)
    data = tickerData.history(period='id', start=start, end=end)
    tickerDf = data
    tickerDf.reset_index(inplace=True)
    lefti, righti = st.columns(2)
    with lefti:
        st.markdown(f"symbol: {tickerData.info['symbol']}" )
        st.markdown(f"longName: {tickerData.info['longName']}")
        st.markdown(f"Sector: {tickerData.info['sector']}")
        st.markdown(f"industry: {tickerData.info['industry']}")
        st.markdown(f"fullTimeEmployees: {tickerData.info['fullTimeEmployees']}")
    with righti:
        st.image(tickerData.info['logo_url'])
        #stock_data = stock_data.append({'symbol': tickerData.info['symbol'], 'longName': tickerData.info['longName'],
        #                                'sector': tickerData.info['sector'], 'industry': tickerData.info['industry'],
        #                                'fullTimeEmployees': tickerData.info['fullTimeEmployees'],
        #                                'logo_url': tickerData.info['logo_url']}, ignore_index=True)
        #stock_data.to_csv(f'{Company}_data.csv')
        #st.write("your csv file saved")

    with st.container():
        st.write("---")
        st.write(f"The last 5 days statistics of {tickerData.info['longName']}")
        st.write(tickerDf.sort_values(by=['Date'], ascending=False).head(5))
        st.write(f'stock **Opening** and **closing** price of {Company}!')
        loading_text.text("Your Stock data is available now!")
        pt.plot_raw_data(tickerDf)

    # **---- Forcasting ----**
    predict_stock = st.button(label='Start the Prediction')
    df = tickerDf[['Date', 'Close']]
    model, forecast = predict_the_stock(df)
    fig1 = plot_plotly(model, forecast)
    st.plotly_chart(fig1)