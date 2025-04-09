from app.services.reddit_service import get_reddit_data_by_date
from app.services.stock_service import get_stock_by_date
import pandas as pd
from flask import jsonify


def get_correlation_metrics(ticker, start_date, end_date):
    print(ticker)
    print(list(start_date))
    print(list(end_date))
    
    # getting reddit and stock data
    # todo: incorporate time frame
    # Get correct data
    reddit_post = get_reddit_data_by_date(ticker, start_date, end_date)
    stocks = get_stock_by_date(ticker, start_date, end_date)

    mapped_reddit_data = []

    mapped_stock_data = []

    for stock in stocks:
        mapped_stock_data.append(
            {
                "date": stock["date"],
                "open": stock["open"],
                "ticker": stock["ticker"],
                "close": stock["close"],
                "high": stock["high"],
                "low": stock["low"],
                "volume": stock["volume"],
            }
        )

    for post in reddit_post:
        RAI = post["number_comments"] + (post["upvote_ratio"] * post["number_upvotes"])
        mapped_reddit_data.append(
            {
                "RedditActivityIndex": RAI,
                "date": post["date_of_creation"],
                "Number_of_comments": post["number_comments"],
                "Upvotes": post["number_upvotes"],
                "UpvotesRatio": post["upvote_ratio"],
                "Sentiment_Score": post["sentiment_score"],
            }
        )

    df_reddit = pd.DataFrame(mapped_reddit_data)
    df_stock = pd.DataFrame(mapped_stock_data)
    # merge similar dates onto one df to compare
    if df_stock is None or df_reddit is None:
        print(df_reddit)
        print(df_stock)

        return []

    if df_stock.empty or df_reddit.empty:

        return []
    df_merged = pd.merge(df_reddit, df_stock, on="date")

    correlated_values = []
    
    correlated_values.append({"volume-sentiment":df_merged['volume'].corr(df_merged['Sentiment_Score'])})
    correlated_values.append({"open-sentiment":df_merged['open'].corr(df_merged['Sentiment_Score'])})
    correlated_values.append({"close-sentiment":df_merged['close'].corr(df_merged['Sentiment_Score'])})
    correlated_values.append({"high-sentiment":df_merged['high'].corr(df_merged['Sentiment_Score'])})
    correlated_values.append({"low-sentiment":df_merged['low'].corr(df_merged['Sentiment_Score'])})    
    correlated_values.append([df_merged.to_dict()])


    correlated_values.append({"volume-RAI":df_merged['volume'].corr(df_merged['RedditActivityIndex'])})
    correlated_values.append({"open-RAI":df_merged['open'].corr(df_merged['RedditActivityIndex'])})
    correlated_values.append({"close-RAI":df_merged['close'].corr(df_merged['RedditActivityIndex'])})
    correlated_values.append({"high-RAI":df_merged['high'].corr(df_merged['RedditActivityIndex'])})
    correlated_values.append({"low-RAI":df_merged['low'].corr(df_merged['RedditActivityIndex'])})
  
    
    """Reddit Activity index"""
    """Number of comments *  number upvotes* upvote ratio"""

    """Sentiment Score per post"""
    """ Sum all scores and divide by total num of comments"""

    return [correlated_values]
