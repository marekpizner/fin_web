from abc import ABC, abstractmethod
import pandas as pd
import psycopg2

from datetime import datetime, timedelta
from sqlalchemy import create_engine


def read_env():
    import os
    database = os.environ['SQL_DATABASE']
    user = os.environ['SQL_USER']
    password = os.environ['SQL_PASSWORD']
    host = os.environ['SQL_HOST']
    port = os.environ['SQL_PORT']

    return database, user, password, host, port


def get_data():
    database, user, password, host, port = read_env()
    conn = psycopg2.connect(
        f'postgresql://{user}:{password}@{host}:{port}/{database}')
    cur = conn.cursor()
    sql_query = """ select * from fin_web_graphs.btc"""
    table = pd.read_sql_query(sql_query, conn)
    return table


class AbstractGraph():

    def __init__(self):
        pass

    def get_config(self):
        pass

    def get_raw_data(self):
        df = get_data()
        return df

    def calculate_data(self):
        pass

    def create_layout(self, data):
        pass

    def get_plot(self, context):
        pass
