from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json

def parse_data(content):
    json_obj = json.loads(content)
    print(json_obj)

    lastest_price = None
    print(json.dumps(json_obj, indent=4))
    if 'msgArray' in json_obj:
        try:
            lastest_price = json_obj['msgArray'][0]['z']
        except KeyError as e:
            lastest_price = json_obj['msgArray'][0]['y']
        except:
            lastest_price = None

    return lastest_price

def get_price(stock_id):
    req = requests.session()
    req.get('http://mis.twse.com.tw/stock/index.jsp')

    tse_query_url = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{}.tw&json=1'
    otc_query_url = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_{}.tw&json=1'

    print(tse_query_url.format(stock_id))
    response = req.get(tse_query_url.format(stock_id))
    price = parse_data(response.text)
    if not price:
        print(otc_query_url.format(stock_id))
        response = req.get(otc_query_url.format(stock_id))
        price = parse_data(response.text)

    return price
