import pandas as pd
import quandl
import os
import psycopg2

from datetime import datetime, timedelta
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


def read_env():
    database = os.environ['SQL_DATABASE']
    user = os.environ['SQL_USER']
    password = os.environ['SQL_PASSWORD']
    host = os.environ['SQL_HOST']
    port = os.environ['SQL_PORT']

    return database, user, password, host, port


def build_postgres_engine():
    database, user, password, host, port = read_env()
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')


def create_schema(schema):
    print('Creating schema')
    database, user, password, host, port = read_env()
    conn = psycopg2.connect(
        f'postgresql://{user}:{password}@{host}:{port}/{database}')
    cur = conn.cursor()
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    conn.commit()
    conn.close()


def save_to_postgres(df, engine, schema, table_name):
    create_schema(schema)
    print('Uploading')
    df.to_sql(table_name, engine, index=False,
              schema=schema, if_exists='replace')


def start():
    data = get_data()
    engine = build_postgres_engine()
    schema = 'fin_web_graphs'
    table_name = 'btc'
    save_to_postgres(data, engine, schema, table_name)


if __name__ == "__main__":
    start()
