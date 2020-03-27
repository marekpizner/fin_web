import pandas as pd
import numpy as np

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

        df['date'] = pd.to_datetime(df['date'])
        df['days'] = df.apply(lambda x: calculate_date_to_halving(x['date']), axis=1)
        max_value_for_year = df.resample('y', on='date').max().dropna(how='all')

        max_value_for_year['year'] = max_value_for_year['date'].apply(lambda x: x.year)
        max_value_for_year['max'] = max_value_for_year['value']
        max_value_for_year.drop(['date', 'value', 'days', ], axis=1, inplace=True)

        df['year'] = df['date'].apply(lambda x: x.year)

        df = df.merge(max_value_for_year, on='year', how='left')

        h2_d = pd.date_range(start=pd.to_datetime("28.4.2013"), end=pd.to_datetime("9.7.2016"), freq='D')
        # h2_v =

        h3_d = pd.date_range(start=pd.to_datetime("10.7.2016"), end=pd.to_datetime("13.5.2020"), freq='D')
        # h3_v =

        # missing_values = pd.DataFrame({"date": dates.date, "value": values})

        # df['stock_to_flow'] = df['mc'] / df['max']
        # print()

        return df

    def create_layout(self, df):
        div = []
        # trace2 = go.Scatter(x=df['date'], y=df['WMA'], marker_color='rgba(0, 255, 0, .8)', mode="lines",
        #                     name='200 Week Moving Average')

        trace3 = go.Scatter(x=df['date'], y=df['value'], mode='markers', marker={
            'size': 12,
            'color': df['days'],
            'colorscale': 'Rainbow',
            'colorbar': {
                "title": {
                    "text": "Dyas to halving",
                    "side": "right"
                }
            },
            'showscale': True
        }, name='% Monthly Increase of 200 Week Moving Average')

        data = go.Data([trace3])
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
        figure.write_image(self.config['icon_path'])
        div = opy.plot(figure, auto_open=False, output_type='div')

        return div

    def get_plot(self, context):
        data = self.calculate_data()
        div = self.create_layout(data)

        context['graph'] = div
        context['title'] = self.config['title']

        return data, context
