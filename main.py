import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PIL import Image
import io

# Title for your Streamlit app
st.title("Streamlit on Replit by Danish")

# Reading the CSV file
hist_df = pd.read_csv('Stock_History.csv')
# Convert the 'Date' column to datetime format (if not already)
hist_df['Date'] = pd.to_datetime(hist_df['Date'])

# Unique tickers
tickers = hist_df['Ticker'].unique()

# Time period selector
time_period = st.selectbox("Select Time Period", 
                           ['3 months', '6 months', '1 year', '5 years', 'All time'])

# Ticker selector
selected_ticker = st.selectbox("Select Ticker", tickers)

# Function to convert plot to image
def plot_to_image(figure):
    buf = io.BytesIO()
    figure.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image = Image.open(buf)
    return image

# Filter data based on ticker
ticker_df = hist_df[hist_df['Ticker'] == selected_ticker]

if not ticker_df.empty:
    # Filter data based on time period
    if time_period != 'All time':
        end_date = ticker_df['Date'].max()
        start_date = {
            '3 months': end_date - timedelta(days=90),
            '6 months': end_date - timedelta(days=180),
            '1 year': end_date - timedelta(days=365),
            '5 years': end_date - timedelta(days=365 * 5)
        }[time_period]
        ticker_df = ticker_df[ticker_df['Date'] >= start_date]

    ticker_df = ticker_df.sort_values(by='Date')

    # Create and display plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    # Main plot with price and moving averages
    ax1.plot(ticker_df['Date'], ticker_df['Price'], label='Price', color='blue')
    ax1.plot(ticker_df['Date'], ticker_df['50d MA'], label='50d MA', color='green')
    ax1.plot(ticker_df['Date'], ticker_df['200d MA'], label='200d MA', color='red')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True)

    # Volume bar plot
    ax2.bar(ticker_df['Date'], ticker_df['Volume'], color='grey', width=1)
    ax2.set_ylabel('Volume')
    ax2.grid(True)

    # Convert plot to image and display
    image = plot_to_image(fig)
    st.image(image, use_column_width=True)
    plt.close(fig)
else:
    st.write(f"No data available for ticker: {selected_ticker}")
