from app.models import StockData
from datetime import datetime

def get_stock_data(ticker):
    try:
        stocks=StockData.query.filter(StockData.ticker == ticker).all()
        return [item.to_dict() for item in stocks]
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None
        

    
def get_stock_by_date(ticker,start_date=None,end_date=None):
    try:
        query = StockData.query.filter(StockData.ticker == ticker)
        if start_date and end_date:
            start = datetime.strptime(start_date,"%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            print(start)
            print(end)
            query = query.filter(StockData.date>=start).filter(StockData.date<=end)
        
        #Query to get a specific recorder by ticker and date
        result = query.all()
        return [item.to_dict() for item in result]
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None
    
