from sqlalchemy import Integer, String, BigInteger,Date,Numeric
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