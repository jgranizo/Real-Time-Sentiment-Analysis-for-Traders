import yfinance as yf
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


now_time = datetime.now().strftime('%Y-%m-%d')
start_time = f"{datetime.now().year - 5}-{datetime.now().month:02d}-{datetime.now().day:02d}"

tickerStrings= ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Example stock list

   



# Download 2 days of data for each ticker, grouping by 'Ticker' to structure the DataFrame with multi-level columns
df = yf.download(tickerStrings, group_by='Ticker', start=start_time,end=now_time)

# Transform the DataFrame: stack the ticker symbols to create a multi-index (Date, Ticker), then reset the 'Ticker' level to turn it into a column
df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)
df.to_csv("ticker.csv")