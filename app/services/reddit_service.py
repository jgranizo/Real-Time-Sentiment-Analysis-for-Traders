import math
import praw
import csv
from datetime import datetime, timedelta, timezone
from app.models import RedditPostData
from app.extensions import db

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
                    "company": company
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
    companies = {"TSLA": "Tesla","MSFT":"Microsoft","APPL": "Apple"}
    if ticker not in companies.keys():
        print("Not a valid ticker")
        return 
    try:
        redditData = RedditPostData.query.filter(RedditPostData.company==companies[ticker]).all()
        return [item.to_dict() for item in redditData]
    except Exception as e:
        db.session.rollback()
        print(f"Error retrieving reddit posts: {e}")
        return None
"""
def get_reddit_metrics(ticker):
    
    sample_posts = [
        {
            "num_comments": 40,
            "ups": 120,
            "upvote_ratio": 0.93,
            "score": 150,
            "total_awards": 2,
            "crossposts": 1,
            "sentiment": 0.76  # Assume you ran NLP on the title/comments
        },
        {
            "num_comments": 20,
            "ups": 80,
            "upvote_ratio": 0.89,
            "score": 90,
            "total_awards": 1,
            "crossposts": 0,
            "sentiment": 0.60
        }
    ]
    total_sentiment=0
    total_activity=0
    total_virality = 0
    count = len(sample_posts)
    
    for post in sample_posts:
        activity = post['num_comments']*post["ups"]* post["upvote_ratio"]
        virality = math.log(post["score"]+1) + post["total_awards"] + post["crossposts"]
        total_sentiment += post["sentiment"]
        total_activity += activity
        total_virality += virality

    avg_sentiment = total_sentiment/ count if count else 0
    avg_activity =total_activity / count if count else 0
    avg_virality = total_virality / count if count else 0
    return{
        "ticker":ticker,
        "activity_index": round(total_activity,2),
        "sentiment_score": round(avg_sentiment,3),
        "virality_score": round(avg_virality,3)

    }

    """
