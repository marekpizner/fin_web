import pandas as pd
import numpy as np

from .abstract_graph import AbstractGraph
import plotly.graph_objs as go
import plotly.offline as opy

CONFIG = {
    'title': 'RSI',
    'url': 'graph/rsi',
    'icon': 'fin_web_graphs/img/rsi.png',
    'icon_path': 'fin_web_graphs/static/fin_web_graphs/img/rsi.png'
}


class RSI(AbstractGraph):

    def __init__(self, window_1, config=CONFIG):
        super().__init__()
        self.window_1 = window_1
        self.config = config

    def get_config(self):
        return self.config

    def get_raw_data(self):
        return super().get_raw_data()

    def calcualte_rsi(self, series, period):
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
        u = u.drop(u.index[:(period - 1)])
        d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
        d = d.drop(d.index[:(period - 1)])
        rs = pd.Series.ewm(u, com=period - 1, adjust=False).mean() / \
             pd.Series.ewm(d, com=period - 1, adjust=False).mean()
        return 100 - 100 / (1 + rs)

    def calculate_data(self):
        df = self.get_raw_data()

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by="date")
        df.set_index(['date'], drop=False, inplace=True)

        rs = self.calcualte_rsi(df['value'], self.window_1)
        rs = pd.DataFrame(rs)
        rs.columns = ['rs']

        df = df.join(rs)
        return df

    def create_layout(self, df):
        trace1 = go.Scatter(x=df['date'], y=df['value'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Price BTC (USD)')
        trace2 = go.Scatter(x=df['date'], y=df['rs'], marker_color='rgba(255, 165, 0, .8)', mode="lines", name='RSI')

        data = go.Data([trace1, trace2])
        layout = go.Layout(title="High",
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

                           yaxis={'title': 'Value',
                                  'showline': True,
                                  'linecolor': 'black',
                                  'linewidth': 2,

                                  "showspikes": True,
                                  "spikesnap": 'data',
                                  "spikethickness": 1,
                                  'spikedash': 'solid',
                                  "spikecolor": 'black',
                                  "tickprefix": "$",
                                  # "tickformat": '<d'
                                  },

                           yaxis_type="log",
                           yaxis_showgrid=False,

                           legend_orientation="h",
                           plot_bgcolor='rgb(255,255,255)',
                           height=800)

        figure = go.Figure(data=data, layout=layout)
        figure.write_image(self.config['icon_path'])
        div = opy.plot(figure, auto_open=False, output_type='div')

        return div

    def get_plot(self, context):
        data = self.calculate_data()
        div = self.create_layout(data)

        context['graph'] = div
        context['title'] = self.config['title']

        return data, context
