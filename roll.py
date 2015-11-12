from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()

def convert_date(date):
    return [int(num) for num in date.split('/')]

class Roll(Base):
    __tablename__ = 'rolls'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    identity = Column(Integer)
    rolldate = Column(Date)
    startdate = Column(Date)
    enddate = Column(Date)
    share = Column(Integer)
    sell = Column(Float)

    def __init__(self, id, name, identity, rolldate, startdate, enddate, share, sell):
        self.id = id
        self.name = name
        self.identity = identity
        self.rolldate = date(*convert_date(rolldate))
        self.startdate = date(*convert_date(startdate))
        self.enddate = date(*convert_date(enddate))
        self.share = share
        self.sell = sell

    def __repr__(self):
        return '%s 抽 %s(%s) %s 股. 價格:%.2f. 開始: %s, 截止: %s' % \
                (self.rolldate, self.name, self.identity, self.share, round(self.sell, 2), self.startdate, self.enddate)

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    aroll = Roll(1, 2412, '中華電', '2015/11/11', '2015/11/01', '2015/11/14', 1000, 50.0)
    print(aroll)
    print('Mapper: ', aroll.__mapper__)
    


