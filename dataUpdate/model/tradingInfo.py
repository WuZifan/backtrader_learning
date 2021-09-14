from dataUpdate import Base
from sqlalchemy import Column, Integer, String,Float,DateTime,Boolean


class TradingInfo(Base):
    __tablename__ = 'TradingInfo'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    code = Column(String(100),index=True)
    time = Column(DateTime,index=True)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    amount = Column(Float)

    def __init__(self, code,time, open, close, high, low, volume, amount):
        self.code = code
        self.time = time
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.amount = amount

    def __repr__(self):
        return "{},{},{}".format(self.time, self.open, self.close)
