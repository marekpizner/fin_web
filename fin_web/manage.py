#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pandas as pd

from fin_web_graphs.models import Olhc

import_file = True


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fin_web.settings')

    if import_file:
        pd_df = pd.read_csv('data.csv', index_col=[0])
        for index, x in pd_df.iterrows():
            olhc = Olhc()
            olhc.date = x['date']
            olhc.open = x['open']
            olhc.high = x['high']
            olhc.low = x['low']
            olhc.close = x['close']
            olhc.volume = x['volume']
            olhc.market_cap = x['market_cap']
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
