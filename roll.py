from sqlalchemy import create_engine
from sqlalchemy import Column, SmallInteger, String, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()

def convert_date(date):
    return [int(num) for num in date.split('/')]

class Roll(Base):
    __tablename__ = 'rolls_roll'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    identity = Column(SmallInteger)
    roll_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    shares = Column(SmallInteger)
    sell_price = Column(Float)
    price = Column(Float)
    market = Column(String)

    def __init__(self, id, name, identity, roll_date, start_date, end_date, shares, sell_price, market):
        self.id = id
        self.name = name
        self.identity = identity
        self.roll_date = date(*convert_date(roll_date))
        self.start_date = date(*convert_date(start_date))
        self.end_date = date(*convert_date(end_date))
        self.shares = shares
        self.sell_price = sell_price
        self.market = market

    def __repr__(self):
        return '%s 抽 %s(%s) %s 股. 價格:%.2f. 開始: %s, 截止: %s' % \
                (self.roll_date, self.name, self.identity, self.shares, round(self.sell_price, 2), self.start_date, self.end_date)

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    aroll = Roll(1, 2412, '中華電', '2015/11/11', '2015/11/01', '2015/11/14', 1000, 50.0)
    print(aroll)
    print('Mapper: ', aroll.__mapper__)
    


