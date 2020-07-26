import pandas as pd
import numpy as np
import math
import os.path as pathh


from .abstract_graph import AbstractGraph
import plotly.graph_objs as go
import plotly.offline as opy

CONFIG = {
    'title': 'Stock to flow',
    'url': 'graph/graph_stock_to_flow',
    'icon': 'fin_web_graphs/img/graph_stock_to_flow.png',
    'icon_path': 'fin_web_graphs/static/fin_web_graphs/img/graph_stock_to_flow.png'
}


class StockToFlow(AbstractGraph):

    def __init__(self, shift, config=CONFIG):
        super().__init__()
        self.shift = shift
        self.config = config

    def get_config(self):
        return self.config

    def get_raw_data(self):
        return super().get_raw_data()

    def calculate_data(self):

        def calculate_date_to_halving(date):
            h1 = pd.to_datetime("28.11.2012")
            h2 = pd.to_datetime("9.7.2016")
            h3 = pd.to_datetime("13.5.2020")

            if date > h2:
                dif = h3 - date
            elif date > h1:
                dif = h2 - date
            else:
                dif = h1 - date
            return dif.days

        df = self.get_raw_data()
        df = df.round(2)

        df['date'] = pd.to_datetime(df['date'])
        df['days'] = df.apply(
            lambda x: calculate_date_to_halving(x['date']), axis=1)
        df['max'] = df.shift(periods=365)['btc_count']
        df['max'] = (df['btc_count'] - df['max'])
        df['stf'] = df['btc_count'] / df['max']

        # Power law formula
        df['stf'] = 0.4 * (df['stf'] * df['stf'] * df['stf'])

        df = df[df['date'] >= pd.to_datetime('31.08.2010')]
        return df

    def is_time_to_save_image(self, figure):
        if not pathh.exists(self.config['icon_path']):
            figure.write_image(self.config['icon_path'])

    def create_layout(self, df):
        trace2 = go.Scatter(x=df['date'], y=df['stf'], marker_color='rgba(255, 60, 60, .8)', mode="lines",
                            name='stock-to-flow (0.4 * STF ^ 3) almost power law')

        trace3 = go.Scatter(x=df['date'], y=df['value'], mode='markers', marker={
            'size': 10,
            'color': df['days'],
            'colorscale': 'Rainbow',
            'colorbar': {
                "title": {
                    "text": "Dyas to halving",
                    "side": "right"
                }
            },
            'showscale': True
        }, name='Price BTC (USD)')

        data = go.Data([trace3, trace2])
        layout = go.Layout(title=self.config['title'],

                           xaxis={'title': 'Date',
                                  'showline': True,
                                  'linecolor': 'black',
                                  'linewidth': 2,

                                  "showspikes": True,
                                  'spikemode': 'across',
                                  "spikesnap": 'cursor',
                                  "spikethickness": 1,
                                  'spikedash': 'solid',
                                  "spikecolor": 'black'

                                  },

                           xaxis_showgrid=True,
                           xaxis_gridcolor='rgba(128,128,128,.5)',

                           yaxis={'title': 'Price BTC (USD)',
                                  'side': 'left',
                                  'showline': True,
                                  'linecolor': 'black',
                                  'linewidth': 2,

                                  "showspikes": True,
                                  "spikesnap": 'data',
                                  "spikethickness": 1,
                                  'spikedash': 'solid',
                                  "spikecolor": 'black',
                                  "tickprefix": "$"
                                  },
                           yaxis_type="log",
                           yaxis_showgrid=False,

                           legend_orientation="h",
                           plot_bgcolor='rgb(255,255,255)',

                           height=800)

        figure = go.Figure(data=data, layout=layout)
        self.is_time_to_save_image(figure)
        div = opy.plot(figure, auto_open=False, output_type='div')

        return div

    def get_plot(self, context):
        data = self.calculate_data()
        div = self.create_layout(data)

        context['graph'] = div
        context['title'] = self.config['title']

        return data, context
