import pandas as pd

from fin_web_graphs.models import Olhc

CSV_PATH = 'data.csv'

Olhc.objects.all().delete()

pd_df = pd.read_csv(CSV_PATH, index_col=[0]).reset_index()
pd_df['date'] = pd.to_datetime(pd_df['date'])

for index, x in pd_df.iterrows():
    print(x.keys())
    olhc = Olhc()
    olhc.date = x['date']
    olhc.open = x['open']
    olhc.high = x['high']
    olhc.low = x['low']
    olhc.close = x['close']
    olhc.volume = x['volume']
    olhc.market_cap = x['market_cap']

    olhc.save()