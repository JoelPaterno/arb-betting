# SQLAlchemy models (database tables)
from sqlalchemy import Column, Integer, String, Float
from db.db import Base

class ArbitrageOpportunity(Base):
    __tablename__ = 'arbitrage_opportunities'

    id = Column(Integer, primary_key=True, index=True)
    match = Column(String, index=True)
    bookmaker1 = Column(String)
    bookmaker2 = Column(String)
    odds1 = Column(Float)
    odds2 = Column(Float)
    profit = Column(Float)