from app.services.reddit_service import get_reddit_metrics
from app.services.stock_service import get_stock_metrics
def get_correlation_metrics(ticker):
    #getting reddit and stock data
    #todo: incorporate time frame
    reddit = get_reddit_metrics(ticker)
    stock = get_stock_metrics(ticker)

    sentiment = reddit["sentiment_score"]
    volatility = stock["volatility"]

    #simple dummy formula for now for correlation score
    correlation = round(sentiment*volatility,3)




    return {
        "ticker":ticker,
        "sentiment_score": sentiment,
        "volatilty":volatility,
        "correlation": correlation, #eventually calculated with real data,
        "activity_index": reddit["activity_index"],
        "virality_score": reddit["virality_score"],
        "price_series": stock["price_series"]

    }
