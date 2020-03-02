# import requests_html
import requests
import pandas as pd
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from fin_web_graphs.models import Olhc


def get_today():
    today = datetime.today() - timedelta(days=1)
    today = today.strftime('%Y%m%d')

    return today


def get_last_from_db():
    last_date = Olhc.objects.latest('date')
    last_date = str(last_date).replace('-', '')

    return last_date


def get_start_end_date_in_db():
    start = get_last_from_db()
    end = get_today()

    return start, end


def create_url(start_date, end_date):
    return 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start={}&end={}'.format(start_date, end_date)


def get_data(url):
    print('downloading')
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all('table')
    table = table[-1]
    data = [[td.text.strip().replace(',', '') for td in tr.findChildren('td')] for tr in table.findChildren('tr')]

    df = pd.DataFrame(data)
    df.columns = ["date",
                  "open",
                  "high",
                  "low",
                  "close",
                  "volume",
                  "market_cap"]
    df.dropna(inplace=True)

    return df


def insert_data_to_db(df):
    print('inserting')
    df['date'] = pd.to_datetime(df['date'])
    # print(df)
    for index, x in df.iterrows():
        # print(x.keys())
        olhc = Olhc()
        olhc.date = x['date']
        olhc.open = x['open']
        olhc.high = x['high']
        olhc.low = x['low']
        olhc.close = x['close']
        olhc.volume = x['volume']
        olhc.market_cap = x['market_cap']

        olhc.save()


def start():
    start_d, end_d = get_start_end_date_in_db()
    print(start_d, end_d)

    if end_d != get_last_from_db():
        url = create_url(start_d, end_d)
        df = get_data(url)
        insert_data_to_db(df)
