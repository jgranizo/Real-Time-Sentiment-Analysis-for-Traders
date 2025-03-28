import math
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