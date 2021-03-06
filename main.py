# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from roll import Roll
import os
from datetime import datetime
from price import get_price

db_path = './roll.db'
open(db_path, 'a').close()
os.utime(db_path)

engine = create_engine('sqlite:///' + db_path, echo=True)
Roll.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

year = str(datetime.now().year)
target_url = 'http://www.twse.com.tw/ch/announcement/download/%sSUMMARIES.xls' % (year)

# Get data from url and store into database
with urlopen(target_url) as target:

    # the roll announce page is encode by big5. What the heck.
    content=target.read().decode('big5', 'ignore')
    soup = BeautifulSoup(content, 'html.parser')
    table=soup.find('table')

    # the table header we don't need, slice it.
    for row in table.find_all('tr')[1:]:
        record = dict()
        columns = row.find_all('td')

        # I don't care bond, which code is 6 digits instead of 4, and skip it.
        if len(columns[3].string) > 4:
            continue

        # skip already exist data.
        last_record = session.query(Roll).order_by(desc("id")).first()
        if last_record is not None and last_record.id >= int(columns[0].string):
            print('nothing new')
            break

        # preapre record data
        aroll = Roll(int(columns[0].string), columns[2].string, columns[3].string,
                columns[1].string, columns[5].string, columns[6].string, 
                int(columns[13].string), float(columns[9].string), columns[4].string)
        session.add(aroll)

    session.commit()

# update target reference price
records = session.query(Roll).filter(Roll.roll_date > datetime.today()).all()
for record in records:
    record.latest_price = get_price(record.identity)
    session.commit()

session.close()
