# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from roll import Roll

engine = create_engine('sqlite:///./roll.db', echo=True)
Roll.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

target_url = 'http://www.twse.com.tw/ch/announcement/download/2015SUMMARIES.xls'

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

        # preapre record data
        aroll = Roll(int(columns[0].string), columns[2].string, columns[3].string,
                columns[1].string, columns[5].string, columns[6].string, 
                int(columns[13].string), float(columns[9].string))
        session.add(aroll)

    session.commit()
