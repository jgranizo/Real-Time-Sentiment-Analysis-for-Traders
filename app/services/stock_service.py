from app.models import StockData
from sqlalchemy.dialects.postgresql import insert;
from datetime import datetime
import yfinance as yf
import pandas as pd
from app.extensions import db




def get_stock_data(ticker):
    try:
        stocks=StockData.query.filter(StockData.ticker == ticker).all()
        return [item.to_dict() for item in stocks]
        
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None
       

def insert_stock_data(df):
    '''
    Efficiently bulk insert a large DataFrame into a SQLAlechemy Model with Conflict handling
    
    Args:
        df(pd.DataFrame): The stock data Dataframe
        chunk_size(int): Number of rows per insertion batch
    '''     
    try:
        i=0
        for row in df.itertuples():
            stmt = {"date":row.date,
                    "open":row.open,
                          "close":row.close,
                          "low":row.low,
                          "volume":row.volume,
                          "high":row.high, 
                          "ticker":row.ticker}
            existing_post = StockData.query.filter_by(ticker=row.ticker,date=row.date).first()

            if existing_post:
                print(f"Duplicate entry: {existing_post}")
                continue
            new_post = StockData(**stmt)
            db.session.add(new_post)
            db.session.commit()
            i+=1
            print(f"Stored Stock post: {i}")
           
    except Exception as e:
        db.session.rollback()
        print(f"Error saving post: {e}")
        return None
    

        

        
       

def fetch_stock_by_date():
    ''' We must first, call the yfinance api to download the data and store it in a df. 
        Then we must iterate through the df to store in the database'''
    tickerStrings=["AAPL", "MSFT", "AMZN", "GOOGL",
        "NVDA", "META", "TSLA", "JPM",
        "JNJ", "V", "UNH", "PG", "XOM",
        "MA", "HD", "BAC", "WMT", "PFE",
        "CVX", "KO", "PEP", "INTC", "ABBV", "CSCO",
        "CMCSA", "NFLX", "ADBE", "CRM", "DIS",
        "T", "VZ", "MRK", "TMO", "ABT", "ACN",
        "MCD", "AVGO", "ORCL", "QCOM", "TXN",
        "COST", "HON", "AMGN", "IBM", "SBUX", "MMM",
        "BA", "CAT", "LMT", "RTX", "GE", "GM",
        "F", "DAL", "AAL", "LUV",
        "MAR", "HLT", "UBER", "LYFT", "ZM", "PLTR",
        "SNOW", "SHOP", "COIN", "ROKU", "SPOT",
        "DKNG", "HOOD", "LCID", "RIVN", "DASH",
        "ABNB", "INTC", "MU", "AMD", "NIO", "BABA",
        "TCEHY", "BIDU", "TM", "SONY", "SSNLF", "003550.KQ",
        "ASML", "TSM", "SAP", "SIEGY", "GSK", "UL",
        "NSRGY", "NVS", "SHEL", "BP", "TTE", "HSBC",
        "BCS", "DB", "UBS"]
    try:        
        end_time = datetime.now().strftime('%Y-%m-%d')
        start_time = f"{datetime.now().year - 5}-{datetime.now().month:02d}-{datetime.now().day:02d}"
        df = yf.download(tickerStrings, group_by='Ticker', start=start_time,end=end_time)
        print("Success downloading data!")

        df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
       
        df = df.rename(columns={"Date":"date","Open":"open","Close":"close","High":"high","Low":"low","Ticker":"ticker","Volume":"volume"})
        df =df.dropna()
        df['date'] = df['date'].dt.date
        df = df[
            (df['open'] >= 0.0) &
            (df['high'] >= 0.0) &
            (df['low'] >= 0.0) &
            (df['close'] >= 0.0) &
            (df['volume'] >= 0.0)
        ]
        threshold = 1e8  # 100 million

        df = df[
            (df['open'].abs() < threshold) &
            (df['high'].abs() < threshold) &
            (df['low'].abs() < threshold) &
            (df['close'].abs() < threshold) &
            (df['volume'].abs() < threshold)
        ]
        df['open'] = df['open'].apply(lambda x: round(x,2))
        df['high'] = df['high'].apply(lambda x: round(x,2))
        df['low'] = df['low'].apply(lambda x: round(x,2))
        df['close'] = df['close'].apply(lambda x: round(x,2))
        df['volume'] = df['volume'].apply(lambda x: round(x,2))

        insert_stock_data(df)
      
        return "success inserting data into database"
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
        
    

def get_stock_by_date(ticker,start_date=None,end_date=None):
    try:
        query = StockData.query.filter(StockData.ticker == ticker)
        if start_date and end_date:
            start = datetime.strptime(start_date,"%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            print(start)
            query = query.filter(StockData.date>=start).filter(StockData.date<=end)
        #Query to get a specific recorder by ticker and date
        result = query.all()
        print(result)
        return [item.to_dict() for item in result]
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None
    
def fetch_yesterday_stocks():
    start_time = f"{datetime.now().year }-{datetime.now().month:02d}-{datetime.now().day-1}"
    end_time = datetime.now().strftime('%Y-%m-%d')
    tickerStrings=["AAPL", "MSFT", "AMZN", "GOOGL",
        "NVDA", "META", "TSLA", "JPM",
        "JNJ", "V", "UNH", "PG", "XOM",
        "MA", "HD", "BAC", "WMT", "PFE",
        "CVX", "KO", "PEP", "INTC", "ABBV", "CSCO",
        "CMCSA", "NFLX", "ADBE", "CRM", "DIS",
        "T", "VZ", "MRK", "TMO", "ABT", "ACN",
        "MCD", "AVGO", "ORCL", "QCOM", "TXN",
        "COST", "HON", "AMGN", "IBM", "SBUX", "MMM",
        "BA", "CAT", "LMT", "RTX", "GE", "GM",
        "F", "DAL", "AAL", "LUV",
        "MAR", "HLT", "UBER", "LYFT", "ZM", "PLTR",
        "SNOW", "SHOP", "COIN", "ROKU", "SPOT",
        "DKNG", "HOOD", "LCID", "RIVN", "DASH",
        "ABNB", "INTC", "MU", "AMD", "NIO", "BABA",
        "TCEHY", "BIDU", "TM", "SONY", "SSNLF", "003550.KQ",
        "ASML", "TSM", "SAP", "SIEGY", "GSK", "UL",
        "NSRGY", "NVS", "SHEL", "BP", "TTE", "HSBC",
        "BCS", "DB", "UBS"]
    try:        
        df = yf.download(tickerStrings, group_by='Ticker', start=start_time,end=end_time)
        print("Success downloading data!")

        df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
       
        df = df.rename(columns={"Date":"date","Open":"open","Close":"close","High":"high","Low":"low","Ticker":"ticker","Volume":"volume"})
        df =df.dropna()
        df['date'] = df['date'].dt.date
        df = df[
            (df['open'] >= 0.0) &
            (df['high'] >= 0.0) &
            (df['low'] >= 0.0) &
            (df['close'] >= 0.0) &
            (df['volume'] >= 0.0)
        ]
        threshold = 1e8  # 100 million

        df = df[
            (df['open'].abs() < threshold) &
            (df['high'].abs() < threshold) &
            (df['low'].abs() < threshold) &
            (df['close'].abs() < threshold) &
            (df['volume'].abs() < threshold)
        ]
        df['open'] = df['open'].apply(lambda x: round(x,2))
        df['high'] = df['high'].apply(lambda x: round(x,2))
        df['low'] = df['low'].apply(lambda x: round(x,2))
        df['close'] = df['close'].apply(lambda x: round(x,2))
        df['volume'] = df['volume'].apply(lambda x: round(x,2))

        insert_stock_data(df)
        print(df.head())
        return "success inserting data into database"
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
        
    
