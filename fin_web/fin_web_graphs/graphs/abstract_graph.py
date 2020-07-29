from abc import ABC, abstractmethod

import pandas as pd
from ..models import Olhc, BTC


class AbstractGraph():

    def __init__(self):
        pass

    def get_config(self):
        pass

    def get_raw_data(self):
        data = BTC.objects.all()
        print('PRINTING !!!')
        print(data)
        date = []
        value = []
        btc_count = []
        btc_mining_diff = []

        for d in data:
            date.append(d.date)
            value.append(float(d.value))
            btc_count.append(float(d.btc_count))
            btc_mining_diff.append(float(d.btc_mining_diff))

        df = pd.DataFrame({"date": date,
                           "value": value,
                           "btc_count": btc_count,
                           "btc_mining_diff": btc_mining_diff
                           })

        df.sort_values(by=['date'], inplace=True)
        return df

    def calculate_data(self):
        pass

    def create_layout(self, data):
        pass

    def get_plot(self, context):
        pass
