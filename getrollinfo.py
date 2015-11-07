# -*- coding: utf-8 -*-
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

# dependencies can be any iterable with strings, 
# e.g. file line-by-line iterator
dependencies = [
    'BeautifulSoup4>=4',
]
pkg_resources.require(dependencies)

from datetime import date
from urllib.request import urlopen
import roll
from bs4 import BeautifulSoup

target_url = 'http://www.twse.com.tw/ch/announcement/download/2015SUMMARIES.xls'

def _date_convert(chinese_date):
    chineseList = chinese_date.split('/')
    year = int(chineseList[0])
    month = int(chineseList[1])
    day = int(chineseList[2])
    return year, month, day

# erase all data in the database
roll.erase()

# Get data from url and store into database
with urlopen(target_url) as target:

    # the roll announce page is encode by big5. What the heck.
    content=target.read().decode('big5', 'ignore')
    soup = BeautifulSoup(content, 'html.parser')
    table=soup.find('table')

    # the table header we don't need
    for row in reversed(table.find_all('tr')):
        # we don't need the 
        record = dict()
        columns = row.find_all('td')

        # if the roll date is overdue. then skip the rest.
        if date.today() > date(*_date_convert(columns[1].string)):
            break

        # I don't care bond, which code is 6 digits instead of 4, and skip it.
        if len(columns[3].string) > 4:
            continue

        # preapre record data
        record['ID'] = columns[0].string
        record['ROLL_DATE'] = date(*_date_convert(columns[1].string))
        record['STOCK_NAME'] = columns[2].string
        record['STOCK_ID'] = columns[3].string
        record['START_DATE'] = date(*_date_convert(columns[5].string))
        record['END_DATE'] = date(*_date_convert(columns[6].string))
        record['SELL_PRICE'] = columns[9].string
        record['SHARE_NUM'] = columns[13].string

        roll.insert(record)

