import pandas as pd
import numpy as np
import os.path as path

from .abstract_graph import AbstractGraph
import plotly.graph_objs as go
import plotly.offline as opy

CONFIG = {
    'title': 'Mining difficulty',
    'url': 'graph/mining_difficulty',
    'icon': 'fin_web_graphs/img/mining_difficulty.png',
    'icon_path': 'fin_web_graphs/static/fin_web_graphs/img/mining_difficulty.png'
}


class MiningDiff(AbstractGraph):

    def __init__(self, config=CONFIG):
        super().__init__()
        self.config = config

    def get_config(self):
        return self.config

    def get_raw_data(self):
        return super().get_raw_data()

    def calculate_data(self):
        df = self.get_raw_data()
        return df

    def is_time_to_save_image(self, figure):
        if not path.exists(self.config['icon_path']):
            figure.write_image(self.config['icon_path'], scale=0.5)

    def create_layout(self, df):
        trace1 = go.Scatter(x=df['date'], y=df['btc_mining_diff'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Mining difficulty')

        data = go.Data([trace1])
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

                           yaxis={'title': 'Difficulty',
                                  'showline': True,
                                  'linecolor': 'black',
                                  'linewidth': 2,

                                  "showspikes": True,
                                  "spikesnap": 'data',
                                  "spikethickness": 1,
                                  'spikedash': 'solid',
                                  "spikecolor": 'black'
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
