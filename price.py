from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_price(stock_id):
    # use cnyes to get the price.
    target_url = 'http://traderoom.cnyes.com/tse/quote2FB.aspx?code=%s' % stock_id
    with urlopen(target_url) as target:
        soup = BeautifulSoup(target.read(), 'html.parser')
        price = soup.find('td', id='currPrice').string
        current_price = 0 if price == '--' else float(price)

    return current_price
