import pandas as pd

import sqlite3
# Create your connection.
cnx = sqlite3.connect('db.sqlite3')

pd_df = pd.read_csv('data.csv', index_col=[0])

print(pd_df.iloc[:2])

pd_df.to_sql(name='fin_web_graphs_olhc', con=cnx)