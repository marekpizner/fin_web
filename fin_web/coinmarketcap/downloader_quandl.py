import pandas as pd
import quandl
import os

from datetime import datetime, timedelta
# from fin_web_graphs.models import BTC
from sqlalchemy import create_engine

QUANDL_KEY = os.environ['QUANDL_KEY']


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
        "BCHAIN/TOTBC", authtoken=QUANDL_KEY)
    number_of_bitcoins.columns = ['btc_count']

    bitcoin_price = quandl.get(
        "BCHAIN/MKPRU", authtoken=QUANDL_KEY)
    bitcoin_price.columns = ['value']

    difficulty_of_mining = quandl.get(
        "BCHAIN/DIFF", authtoken=QUANDL_KEY)
    difficulty_of_mining.columns = ['btc_mining_diff']

    final_df = number_of_bitcoins
    final_df = final_df.join(bitcoin_price)
    final_df = final_df.join(difficulty_of_mining)

    final_df['date'] = final_df.index
    final_df.round(5)
    return final_df


# def insert_data_to_db(df):
#     BTC.objects.all().delete()
#     print("importing data")
#     for index, x in df.iterrows():
#         btc = BTC()

#         btc.date = x['date']
#         btc.value = x['value']
#         btc.btc_count = x['btc_count']
#         btc.btc_mining_diff = x['btc_mining_diff']

#         btc.save()


def build_postgres_engine():
    database = os.environ['SQL_DATABASE']
    user = os.environ['SQL_USER']
    password = os.environ['SQL_PASSWORD']
    host = os.environ['SQL_HOST']
    port = os.environ['SQL_PORT']

    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')


def save_to_postgres(df, engine, table_name):
    df.to_sql(table_name, engine)


def start():
    data = get_data()
    engine = build_postgres_engine()
    table_name = 'BTC'
    save_to_postgres(data, engine, table_name)
    # insert_data_to_db(data)
