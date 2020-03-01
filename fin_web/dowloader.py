# import requests_html
from bs4 import BeautifulSoup
import requests
import pandas as pd

name = "ohlc"
start_date = "20180428"
end_date = "20200208"

url = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start={}&end={}'.format(start_date, end_date)

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
pass
