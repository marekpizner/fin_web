import pandas as pd
import plotly.graph_objs as go
import plotly.offline as opy
import math
import os.path as pathh

from .abstract_graph import AbstractGraph


CONFIG = {
    'title': '2-Year MA Multiplier',
    'url': 'graph/graph_moving_average',
    'icon': 'fin_web_graphs/img/graph_moving_average.png',
    'icon_path': 'fin_web_graphs/static/fin_web_graphs/img/graph_moving_average.png'
}


class MovingAverage(AbstractGraph):

    def __init__(self, window_1, window_2, multiplier=5, config=CONFIG):
        super().__init__()
        self.window_1 = window_1
        self.window_2 = window_2
        self.multiplier = multiplier
        self.config = config

    def get_config(self):
        return self.config

    def get_raw_data(self):
        return super().get_raw_data()

    def calculate_data(self):
        df = self.get_raw_data()

        df['EMA'] = df['value'].rolling(window=self.window_2).mean()
        df['EMA2'] = df['value'].rolling(
            window=self.window_2).mean() * self.multiplier

        df = df[df['date'] >= pd.to_datetime('30.12.2010')]
        return df

    def is_time_to_save_image(self, figure):
        if not pathh.exists(self.config['icon_path']):
            figure.write_image(self.config['icon_path'])

    def create_layout(self, df):
        trace1 = go.Scatter(x=df['date'], y=df['value'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Price BTC (USD)')

        trace2 = go.Scatter(x=df['date'], y=df['EMA'], marker_color='rgba(0, 255, 0, .8)', mode="lines",
                            name='Moving average 2 year')

        trace3 = go.Scatter(x=df['date'], y=df['EMA2'], marker_color='rgba(255, 0, 0, .8)', mode="lines",
                            name=f"Moving average 2 years * {self.multiplier}")

        data = go.Data([trace1, trace2, trace3])

        layout = go.Layout(title="Bitcoin Investor Tool: 2-Year MA Multiplier",

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
                                  'side': 'right',
                                  'showline': True,
                                  'linecolor': 'black',
                                  'linewidth': 2,
                                  "showspikes": True,
                                  "spikesnap": 'data',
                                  "spikethickness": 1,
                                  'spikedash': 'solid',
                                  "spikecolor": 'black',
                                  "tickprefix": "$",
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
