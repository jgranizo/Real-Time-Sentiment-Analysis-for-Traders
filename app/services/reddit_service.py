import math
import praw
import csv
from datetime import datetime, timedelta, timezone
from app.models import RedditPostData
from app.extensions import db
from app.services.predict import predict
import json
import os
import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForTokenClassification

# Initialize Reddit API client with your credentials
reddit = praw.Reddit(
    client_id="ZPr2EshdHCAQUHQ1B4LRdQ",
    client_secret="D_pSNQdQpLFu0xkme74Sket1zGUorg",
    user_agent="BrandDataCollector/1.0 by u/jgran",
)

# Define criteria
brand_name = [
    "Apple", "Microsoft", "Amazon", "Google",
    "Nvidia", "Meta", "Tesla", "Berkshire Hathaway", "JP Morgan",
    "Johnson & Johnson", "Visa", "UnitedHealth", "Procter & Gamble", "Exxon",
    "Mastercard", "Home Depot", "Bank of America", "Walmart", "Pfizer",
    "Chevron", "Coca Cola", "Pepsi", "Intel", "AbbVie", "Cisco",
    "Comcast", "Netflix", "Adobe", "Salesforce", "Disney",
    "AT&T", "Verizon", "Merck", "Thermo Fisher", "Abbott", "Accenture",
    "McDonald's", "Broadcom", "Oracle", "Qualcomm", "Texas Instruments",
    "Costco", "Honeywell", "Amgen", "IBM", "Starbucks", "3M",
    "Boeing", "Caterpillar", "Lockheed Martin", "Raytheon", "GE", "GM",
    "Ford", "Delta Airlines", "American Airlines", "Southwest Airlines",
    "Marriott", "Hilton", "Uber", "Lyft", "Zoom", "Palantir",
    "Snowflake", "Shopify", "Block", "Coinbase", "Roku", "Spotify",
    "DraftKings", "Robinhood", "Lucid", "Rivian", "DoorDash",
    "Airbnb", "Intel", "Micron", "AMD", "NIO", "Alibaba",
    "Tencent", "Baidu", "Toyota", "Sony", "Samsung", "LG",
    "ASML", "TSMC", "SAP", "Siemens", "GSK", "Unilever",
    "Nestle", "Novartis", "Shell", "BP", "TotalEnergies", "HSBC",
    "Barclays", "Deutsche Bank", "UBS",
    "AAPL", "MSFT", "AMZN", "GOOGL",
    "NVDA", "META", "TSLA", "BRK.B", "JPM",
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
    "SNOW", "SHOP", "SQ", "COIN", "ROKU", "SPOT",
    "DKNG", "HOOD", "LCID", "RIVN", "DASH",
    "ABNB", "INTC", "MU", "AMD", "NIO", "BABA",
    "TCEHY", "BIDU", "TM", "SONY", "SSNLF", "003550.KQ",
    "ASML", "TSM", "SAP", "SIEGY", "GSK", "UL",
    "NSRGY", "NVS", "SHEL", "BP", "TTE", "HSBC",
    "BCS", "DB", "UBS"
]

company_ticker_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Nvidia": "NVDA",
    "Meta": "META",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK.B",
    "JP Morgan": "JPM",
    "Johnson & Johnson": "JNJ",
    "Visa": "V",
    "UnitedHealth": "UNH",
    "Procter & Gamble": "PG",
    "Exxon": "XOM",
    "Mastercard": "MA",
    "Home Depot": "HD",
    "Bank of America": "BAC",
    "Walmart": "WMT",
    "Pfizer": "PFE",
    "Chevron": "CVX",
    "Coca Cola": "KO",
    "Pepsi": "PEP",
    "Intel": "INTC",
    "AbbVie": "ABBV",
    "Cisco": "CSCO",
    "Comcast": "CMCSA",
    "Netflix": "NFLX",
    "Adobe": "ADBE",
    "Salesforce": "CRM",
    "Disney": "DIS",
    "AT&T": "T",
    "Verizon": "VZ",
    "Merck": "MRK",
    "Thermo Fisher": "TMO",
    "Abbott": "ABT",
    "Accenture": "ACN",
    "McDonald's": "MCD",
    "Broadcom": "AVGO",
    "Oracle": "ORCL",
    "Qualcomm": "QCOM",
    "Texas Instruments": "TXN",
    "Costco": "COST",
    "Honeywell": "HON",
    "Amgen": "AMGN",
    "IBM": "IBM",
    "Starbucks": "SBUX",
    "3M": "MMM",
    "Boeing": "BA",
    "Caterpillar": "CAT",
    "Lockheed Martin": "LMT",
    "Raytheon": "RTX",
    "GE": "GE",
    "GM": "GM",
    "Ford": "F",
    "Delta Airlines": "DAL",
    "American Airlines": "AAL",
    "Southwest Airlines": "LUV",
    "Marriott": "MAR",
    "Hilton": "HLT",
    "Uber": "UBER",
    "Lyft": "LYFT",
    "Zoom": "ZM",
    "Palantir": "PLTR",
    "Snowflake": "SNOW",
    "Shopify": "SHOP",
    "Block": "SQ",
    "Coinbase": "COIN",
    "Roku": "ROKU",
    "Spotify": "SPOT",
    "DraftKings": "DKNG",
    "Robinhood": "HOOD",
    "Lucid": "LCID",
    "Rivian": "RIVN",
    "DoorDash": "DASH",
    "Airbnb": "ABNB",
    "Micron": "MU",
    "AMD": "AMD",
    "NIO": "NIO",
    "Alibaba": "BABA",
    "Tencent": "TCEHY",
    "Baidu": "BIDU",
    "Toyota": "TM",
    "Sony": "SONY",
    "Samsung": "SSNLF",
    "LG": "003550.KQ",
    "ASML": "ASML",
    "TSMC": "TSM",
    "SAP": "SAP",
    "Siemens": "SIEGY",
    "GSK": "GSK",
    "Unilever": "UL",
    "Nestle": "NSRGY",
    "Novartis": "NVS",
    "Shell": "SHEL",
    "BP": "BP",
    "TotalEnergies": "TTE",
    "HSBC": "HSBC",
    "Barclays": "BCS",
    "Deutsche Bank": "DB",
    "UBS": "UBS"
}

min_score = 1  # Minimum score to filter high-upvote posts
min_comments = 1  # Minimum number of comments for high engagement
days_limit = 1000  # Only get posts from the last 1000 days

# Calculate the Unix timestamp for the date limit
start_date = datetime.now(timezone.utc) - timedelta(days=days_limit)
timestamp_limit_start = start_date.timestamp()
end_date = datetime.now(timezone.utc)
timestamp_limit_end = end_date.timestamp()
# Search for posts mentioning the brand in relevant subreddits
subreddits = ["technology", "gadgets", "stocks",'investing','wallstreetbets','StockMarket','SecurityAnalysis','options','superstonk','shortsueeze','PennyStocks','ValueInvesting','financialindependence','Economics','bogleheads','DividendInvesting','quant','stocksDD','techStocks','WallstreetbetsELITE']
posts_data = []
subreddit_dictionary = {}



#setting up model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
base_dir = os.path.dirname(os.path.abspath(__file__))  # location of the current file
model_dir = os.path.join(base_dir,"..", "SentimentalModel")
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir).to(device)
model.eval()

def preProcessed(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '[URL]', text)
    text = re.sub(r'@\w+', '[USER]', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculateSentimentValues(comments):
    sentiments = {1:0,2:0,3:0}
    #negative-0    neutral-1,        positive-2

    #each comment increments a counter for its corresponding sentiment
    if not comments:
        return sentiments
    preprocessed = [preProcessed(c) for c in comments]

    #Batch tokenize
    encoded = tokenizer(
        preprocessed,
        padding=True,
        truncation=True,
        max_length=140,
        return_tensors='pt'
    )
    input_ids = encoded['input_ids'].to(device)
    attention_mask = encoded['attention_mask'].to(device)


    with torch.no_grad():
        outputs=model(input_ids,attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits,dim=1).tolist()
    
    label_mapping = {0:1,1:2,2:3}
    for raw_pred in predictions:
        sentiment = label_mapping[raw_pred]
        sentiments[sentiment]+=1
    return sentiments
    

def fetch_reddit_post():
    for subreddit_name in subreddits:
        print(f"\nFetching posts about `{brand_name}` in r/{subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)

        # Filter posts based on criteria
        for company in brand_name:

            #saving the company name and ticker to store in the db
            if company in company_ticker_dict:
                company_name = company
                ticker = company_ticker_dict[company_name]
            else:
                ticker = company
                company_name = list(company_ticker_dict.keys())[list(company_ticker_dict.values()).index(ticker)]
                

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
                    print(SentimentMap,"---------------------")
                    positive_comments=SentimentMap[3]
                    neutral_comments=SentimentMap[2]
                    negative_comments=SentimentMap[1]
                    
                    positive_comments_score = SentimentMap[3]*3
                    neutral_comments_score = SentimentMap[2]*2
                    negative_comments_score = SentimentMap[1]
                    sentiment_score = (positive_comments_score+neutral_comments_score+negative_comments_score)/len(comments)
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
                    "company": company_name,
                    "ticker":ticker,
                    "sentiment_score":sentiment_score,
                    "positive_comments":positive_comments,
                    "negative_comments":negative_comments,
                    "neutral_comments": neutral_comments
                        }
                    try:
                        new_post = RedditPostData(**post_info)
                        db.session.add(new_post)
                        db.session.commit()
                        print(f"Stored post: {post.title} from r/{subreddit_name} Company Name: {company_name} Ticker: {ticker}")
                        
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error saving post: {e}")



def get_reddit_data(ticker):
    uppercaseTicker = str(ticker).upper()
    companies = {"TSLA": "Tesla","MSFT":"Microsoft","AAPL": "Apple"}
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
    companies = {"TSLA": "Tesla","MSFT":"Microsoft","AAPL": "Apple"}
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
