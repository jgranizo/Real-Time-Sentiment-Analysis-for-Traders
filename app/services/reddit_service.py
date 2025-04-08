import math
import praw
import csv
from datetime import datetime, timedelta, timezone
from app.models import RedditPostData
from app.extensions import db
from app.services.predict import predict
# Initialize Reddit API client with your credentials
reddit = praw.Reddit(
    client_id="ZPr2EshdHCAQUHQ1B4LRdQ",
    client_secret="D_pSNQdQpLFu0xkme74Sket1zGUorg",
    user_agent="BrandDataCollector/1.0 by u/jgran",
)

# Define criteria
brand_name = ["Tesla", "Microsoft", "Amazon", "Apple"]
min_score = 1  # Minimum score to filter high-upvote posts
min_comments = 1  # Minimum number of comments for high engagement
days_limit = 1000  # Only get posts from the last 7 days

# Calculate the Unix timestamp for the date limit
start_date = datetime.now(timezone.utc) - timedelta(days=days_limit)
timestamp_limit_start = start_date.timestamp()
end_date = datetime.now(timezone.utc)
timestamp_limit_end = end_date.timestamp()
# Search for posts mentioning the brand in relevant subreddits
subreddits = ["technology", "gadgets", "stocks"]
posts_data = []
subreddit_dictionary = {}

def calculateSentimentValues(comments):
    sentiments = {0:0,1:0,2:0}
    #negative-0    neutral-1,        positive-2

    #each comment increments a counter for its corresponding sentiment
    for comment in comments:
        sentiment_value = predict(comment)
        sentiments[sentiment_value]+=1

    return sentiments
    

def fetch_reddit_post():
    for subreddit_name in subreddits:
        print(f"\nFetching posts about `{brand_name}` in r/{subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)

        # Filter posts based on criteria
        for company in brand_name:
            for post in subreddit.search(company):
                if (
                post.created_utc >= timestamp_limit_start
                and post.created_utc <= timestamp_limit_end
                ):
                    existing_post = RedditPostData.query.filter_by(post_id=post.id).first()
                    if existing_post:
                        print(f"Duplicate post detected: {post.title} - Skipping")
                        continue
                    post.comment_sort = 'top'
                    post.comments.replace_more(limit=0)
                    comments = [comment.body for comment in post.comments]
                    SentimentMap=calculateSentimentValues(comments)
                    sentiment_score = len(comments)/3
                    positive_comments = SentimentMap[2]
                    neutral_comments = SentimentMap[1]
                    negative_comments = SentimentMap[0]
                    post_info = {
                    "title": post.title,
                    "score": post.score,
                    "number_comments": post.num_comments,
                    "date_of_creation": datetime.fromtimestamp(
                        post.created_utc
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "subreddit_name": post.subreddit.display_name,
                    "url": post.url,
                    "number_upvotes": post.ups,
                    "upvote_ratio": post.upvote_ratio,
                    "num_cross_posts": post.num_crossposts,
                    "post_id": post.id,
                    "company": company,
                    "sentiment_score":sentiment_score,
                    "positive_comments":positive_comments,
                    "negative_comments":negative_comments,
                    "neutral_comments": neutral_comments
                        }
                    try:
                        new_post = RedditPostData(**post_info)
                        db.session.add(new_post)
                        db.session.commit()
                        print(f"Stored post: {post.title} from r/{subreddit_name}")
                        
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error saving post: {e}")



def get_reddit_data(ticker):
    uppercaseTicker = str(ticker).upper()
    companies = {"TSLA": "Tesla","MSFT":"Microsoft","APPL": "Apple"}
    if uppercaseTicker not in companies.keys():
        print("Not a valid ticker")
        return 
    try:
        redditData = RedditPostData.query.filter(RedditPostData.company==companies[uppercaseTicker]).all()
        return [item.to_dict() for item in redditData]
    except Exception as e:
        db.session.rollback()
        print(f"Error retrieving reddit posts: {e}")
        return None

def get_reddit_data_by_date(ticker,start_date=None,end_date=None):
    uppercaseTicker = str(ticker).upper()
    companies = {"TSLA": "Tesla","MSFT":"Microsoft","APPL": "Apple"}
    if uppercaseTicker not in companies.keys():
        print("Not a valid ticker")
        return 
    try:
        query = RedditPostData.query.filter(RedditPostData.company == companies[uppercaseTicker])
        if start_date and end_date:
            start = datetime.strptime(start_date,"%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(RedditPostData.date_of_creation>=start).filter(RedditPostData.date_of_creation<=end)

        result = query.all()
        return [item.to_dict() for item in result]
    except Exception as e:
        db.session.rollback()
        print(f"Error retrieving reddit posts: {e}")
        return None
