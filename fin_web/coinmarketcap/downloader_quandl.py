import pandas as pd
import quandl

from datetime import datetime, timedelta
from fin_web_graphs.models import BTC


def downloader_handler(funct):
    def funct_wrapper(*args, **kwargs):
        result = []
        for _ in range(5):
            try:
                result = funct(*args, **kwargs)
            except Exception as e:
                print(e)
                continue
            else:
                break
        return result

    return funct_wrapper


@downloader_handler
def get_data():
    number_of_bitcoins = quandl.get(
        "BCHAIN/TOTBC", authtoken="qrqwdqyPspGBV2MKUy9f")
    number_of_bitcoins.columns = ['btc_count']

    bitcoin_price = quandl.get(
        "BCHAIN/MKPRU", authtoken="qrqwdqyPspGBV2MKUy9f")
    bitcoin_price.columns = ['value']

    difficulty_of_mining = quandl.get(
        "BCHAIN/DIFF", authtoken="qrqwdqyPspGBV2MKUy9f")
    difficulty_of_mining.columns = ['btc_mining_diff']

    final_df = number_of_bitcoins
    final_df = final_df.join(bitcoin_price)
    final_df = final_df.join(difficulty_of_mining)

    final_df['date'] = final_df.index
    final_df.round(5)
    return final_df


def insert_data_to_db(df):
    BTC.objects.all().delete()
    print("importing data")
    for index, x in df.iterrows():
        btc = BTC()

        btc.date = x['date']
        btc.value = x['value']
        btc.btc_count = x['btc_count']
        btc.btc_mining_diff = x['btc_mining_diff']

        btc.save()
    pass


def start():
    data = get_data()
    insert_data_to_db(data)
