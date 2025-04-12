from sqlalchemy import Integer, String, BigInteger,Date,Numeric,Float,DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .extensions import db
class StockData(db.Model):
    __tablename__ = 'stocks'
    date: Mapped[Date] = mapped_column(Date, primary_key=True, nullable=False)
    ticker: Mapped[str] = mapped_column(String(10), primary_key=True, nullable=False)
    open: Mapped[float] = mapped_column(Numeric(10, 2))
    high: Mapped[float] = mapped_column(Numeric(10, 2))
    low: Mapped[float] = mapped_column(Numeric(10, 2))
    close: Mapped[float] = mapped_column(Numeric(10, 2))
    volume: Mapped[int] = mapped_column(BigInteger)

    def to_dict(self):
        return {
           "date": str(self.date),
            "ticker": self.ticker,
            "open": float(self.open) if self.open else None,
            "high": float(self.high) if self.high else None,
            "low": float(self.low) if self.low else None,
            "close": float(self.close) if self.close else None,
            "volume": self.volume
        }

    def __repr__(self):
        return f"<StockData(date={self.date}, ticker={self.ticker})>"
    
class RedditPostData(db.Model):
    __tablename__ = 'reddit_posts'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
     # Reddit post ID (unique identifier from Reddit)
    post_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    number_comments: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_creation: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    subreddit_name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    number_upvotes: Mapped[int] = mapped_column(Integer, nullable=False)
    upvote_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    num_cross_posts: Mapped[int] = mapped_column(Integer, nullable=False)
    company: Mapped[str] = mapped_column(String, nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float,nullable=False)
    positive_comments: Mapped[int] = mapped_column(Integer, nullable=False)
    neutral_comments: Mapped[int] = mapped_column(Integer, nullable=False)
    negative_comments: Mapped[int] = mapped_column(Integer, nullable=False)
    ticker: Mapped[str] = mapped_column(String, nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "title": self.title,
            "score": self.score,
            "number_comments": self.number_comments,
            "date_of_creation": self.date_of_creation.strftime('%Y-%m-%d'),
            "subreddit_name": self.subreddit_name,
            "url": self.url,
            "number_upvotes": self.number_upvotes,
            "upvote_ratio": self.upvote_ratio,
            "num_cross_posts": self.num_cross_posts,
            "company": self.company,
            "ticker":self.ticker,
            "sentiment_score": self.sentiment_score,
            "negative_comments": self.negative_comments,
            "positive_comments": self.positive_comments,
            "neutral_comments": self.neutral_comments
        }

    def __repr__(self):
        return f"<RedditPostData(title={self.title}, subreddit={self.subreddit_name})>"