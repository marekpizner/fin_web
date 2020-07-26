import pandas as pd
import numpy as np
import os.path as pathh

from .abstract_graph import AbstractGraph
import plotly.graph_objs as go
import plotly.offline as opy

CONFIG = {
    'title': '200 Week MA',
    'url': 'graph/graph_week_moving_average',
    'icon': 'fin_web_graphs/img/graph_week_moving_average.png',
    'icon_path': 'fin_web_graphs/static/fin_web_graphs/img/graph_week_moving_average.png'
}


class WeeklyMovingAverage(AbstractGraph):

    def __init__(self, shift, config=CONFIG):
        super().__init__()
        self.shift = shift
        self.config = config

    def get_config(self):
        return self.config

    def get_raw_data(self):
        return super().get_raw_data()

    def calculate_data(self):
        df = self.get_raw_data()

        df.sort_values(by=['date'], inplace=True)
        df['WMA'] = df['value'].rolling(window=self.shift).mean()
        df = df.iloc[self.shift:]
        df.drop_duplicates(subset='date', keep='first', inplace=True)

        df_moving_average_heat_m = df.set_index('date')
        df_moving_average_heat_m.index = pd.to_datetime(
            df_moving_average_heat_m.index)
        df_moving_average_heat_m['date'] = df_moving_average_heat_m.index.date
        df_moving_average_heat_m = df_moving_average_heat_m.resample(
            'M').ffill()
        df_moving_average_heat_m['change'] = df_moving_average_heat_m['WMA'].pct_change(
            periods=1) * 100

        return df, df_moving_average_heat_m

    def is_time_to_save_image(self, figure):
        if not pathh.exists(self.config['icon_path']):
            figure.write_image(self.config['icon_path'])

    def create_layout(self, df):
        df, dd = df

        trace1 = go.Scatter(x=df['date'], y=df['value'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Price BTC (USD)')

        trace2 = go.Scatter(x=df['date'], y=df['WMA'], marker_color='rgba(0, 255, 0, .8)', mode="lines",
                            name='200 Week Moving Average')

        trace3 = go.Scatter(x=dd['date'], y=dd['value'], mode='markers', marker={
            'size': 12,
            'color': dd['change'],
            'colorscale': 'Rainbow',
            'colorbar': {
                "title": {
                    "text": "% Monthly Increase of 200 Week Moving Average",
                    "side": "right"
                }
            },
            'showscale': True
        }, name='% Monthly Increase of 200 Week Moving Average')

        data = go.Data([trace1, trace2, trace3])

        layout = go.Layout(title="200 Week Moving Average Heatmap",

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
