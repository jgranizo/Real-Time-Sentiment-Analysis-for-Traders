from app.services.reddit_service import get_reddit_data_by_date
from app.services.stock_service import get_stock_by_date
def get_correlation_metrics(ticker,start_date,end_date):
    #getting reddit and stock data
    #todo: incorporate time frame
    #Get correct data
  reddit_post = get_reddit_data_by_date(ticker,start_date,end_date)
  stocks = get_stock_by_date(ticker,start_date,end_date)

  mapped_reddit_data={"RedditActivityIndex":[],"Creation_date": []
                      ,"Number_of_comments":[],"Upvotes": [],"UpvotesRatio":[], "Sentiment_Score":[]}
  for post in reddit_post:
    RAI = post["number_comments"] +( post["upvote_ratio"] * post["number_upvotes"])
    mapped_reddit_data["RedditActivityIndex"].append(RAI)
    mapped_reddit_data["Creation_date"].append(post["date_of_creation"])
    mapped_reddit_data["Number_of_comments"].append(post["number_comments"])
    mapped_reddit_data["Upvotes"].append(post["number_upvotes"])
    mapped_reddit_data["UpvotesRatio"].append(post["upvote_ratio"])
    mapped_reddit_data["Sentiment_Score"].append(post["sentiment_score"])

  '''Reddit Activity index'''
  '''Number of comments *  number upvotes* upvote ratio'''

  '''Sentiment Score per post'''
  ''' Sum all scores and divide by total num of comments'''
  return mapped_reddit_data
