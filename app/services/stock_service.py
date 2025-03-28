def get_stock_metrics(ticker):
    #simulate historical stock prices over 7 days
    sample_prices = [152.1, 150.3,149.8,151.2,153.0,150.9,152.7]

    mean_price = sum(sample_prices)/len(sample_prices)

    variance = sum((p-mean_price) ** 2 for p in sample_prices)/len(sample_prices)
    volatility = variance ** 0.5


    return{
        "ticker": ticker,
        "average_price": round(mean_price,2),
        "volatility":round(volatility,3),
        "price_series":sample_prices
    }