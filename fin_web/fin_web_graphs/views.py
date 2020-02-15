import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as opy
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Olhc

list_of_graphs = [
    {
        'title': '2-Year MA Multiplier',
        'url': 'graph_open',
        'icon': 'fin_web_graphs/img/b.png'
    },
    {
        'title': '200 Week Moving Average Heatmap',
        'url': 'graph_close',
        'icon': 'fin_web_graphs/img/r.png'
    },
    {
        'title': 'High',
        'url': 'graph_high',
        'icon': 'fin_web_graphs/img/g.png'
    }
]


def index(request):
    context = {
    }

    return render(request, 'fin_web_graphs/index.html', context)


def graphs(request):
    context = {
        'graphs': list_of_graphs
    }

    return render(request, 'fin_web_graphs/graphs.html', context)


def about_us(request):
    context = {}
    return render(request, 'fin_web_graphs/about.html', context)


class GraphOpen(TemplateView):
    template_name = 'fin_web_graphs/graph.html'

    def get_context_data(self, **kwargs):
        data = Olhc.objects.all()

        context = super(GraphOpen, self).get_context_data(**kwargs)
        x = []
        y = []

        for d in data:
            x.append(d.date)
            y.append((float(d.high) + float(d.low)) / 2)
        df = pd.DataFrame({"date": x, "value": y})
        df = df.iloc[::-1]

        df['EMA'] = df['value'].rolling(window=365).mean()
        df['EMA2'] = df['value'].rolling(window=365 * 2).mean() * 5

        # ['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx',
        #  'toself', 'tonext']

        trace1 = go.Scatter(x=df['date'], y=df['value'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Price BTC (USD)')

        trace2 = go.Scatter(x=df['date'], y=df['EMA'], marker_color='rgba(0, 255, 0, .8)', mode="lines",
                            name='Moving average 1 year')

        trace3 = go.Scatter(x=df['date'], y=df['EMA2'], marker_color='rgba(255, 0, 0, .8)', mode="lines",
                            name="Moving average 2 years * 5")

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
                                  "spikecolor": 'black'
                                  },
                           yaxis_type="log",
                           yaxis_showgrid=False,

                           legend_orientation="h",
                           plot_bgcolor='rgb(255,255,255)',

                           height=800)

        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Bitcoin Investor Tool: 2-Year MA Multiplier'
        return context


class GraphClose(TemplateView):
    template_name = 'fin_web_graphs/graph.html'

    def get_context_data(self, **kwargs):
        data = Olhc.objects.all()

        context = super(GraphClose, self).get_context_data(**kwargs)
        x = []
        y = []

        for d in data:
            x.append(d.date)
            y.append((float(d.high) + float(d.low)) / 2)

        df = pd.DataFrame({"date": x, "value": y})
        df = df.iloc[::-1]

        dates = pd.date_range(end=df.iloc[0]['date'], periods=1400, freq='D')
        values = np.sort(np.random.randint(df[:100]['value'].min(), df[:100]['value'].max(), len(dates)))

        df2 = pd.DataFrame({"date": dates.date, "value": values})
        df = df.append(df2)
        df.sort_values(by=['date'], inplace=True)

        df['WMA'] = df['value'].rolling(window=1400).mean()
        df = df.iloc[1400:]

        dd = df.set_index('date')
        dd.index = pd.to_datetime(dd.index)

        dd['date'] = dd.index.date

        dd = dd.resample('M').ffill()
        dd['change'] = dd['WMA'].pct_change(periods=1) * 100

        trace1 = go.Scatter(x=df['date'], y=df['value'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Price BTC (USD)')

        trace2 = go.Scatter(x=df['date'], y=df['WMA'], marker_color='rgba(0, 255, 0, .8)', mode="lines",
                            name='Moving average 1 year')

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
                                  "spikecolor": 'black'
                                  },
                           yaxis_type="log",
                           yaxis_showgrid=False,

                           legend_orientation="h",
                           plot_bgcolor='rgb(255,255,255)',

                           height=800)

        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = '200 Week Moving Average Heatmap'
        return context


class GraphHigh(TemplateView):
    template_name = 'fin_web_graphs/graph.html'

    def get_context_data(self, **kwargs):
        data = Olhc.objects.all()

        context = super(GraphHigh, self).get_context_data(**kwargs)
        x = []
        y = []

        for d in data:
            x.append(d.date)
            y.append(float(d.high))

        trace1 = go.Scatter(x=x, y=y, marker_color='rgba(0, 255, 0, .8)', mode="lines")

        data = go.Data([trace1])
        layout = go.Layout(title="High", xaxis={'title': 'Date'}, yaxis={'title': 'Value'}, height=800)
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph high'
        return context
