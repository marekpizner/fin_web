from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic import TemplateView

import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go

from .models import Olhc

list_of_graphs = [
    {
        'title': 'Open',
        'url': 'graph_open',
        'icon': 'fin_web_graphs/img/b.png'
    },
    {
        'title': 'Close',
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
            y.append(float(d.open))
        df = pd.DataFrame({"date": x, "value": y})
        df = df.iloc[::-1]

        df['EMA'] = df['value'].rolling(window=365).mean()
        df['EMA2'] = df['value'].rolling(window=365 * 2).mean() * 5

        # ['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx',
        #  'toself', 'tonext']

        trace1 = go.Scatter(x=df['date'], y=df['value'], marker_color='rgba(0, 0, 255, .8)', mode="lines",
                            name='Price BTC (USD)',
                            fill=None)

        trace2 = go.Scatter(x=df['date'], y=df['EMA'], marker_color='rgba(0, 255, 0, .8)', mode="lines",
                            name='Moving average 1 year')

        trace3 = go.Scatter(x=df['date'], y=df['EMA2'], marker_color='rgba(255, 0, 0, .8)', mode="lines",
                            name="Moving average 2 years * 5")

        data = go.Data([trace1, trace2, trace3])

        layout = go.Layout(title="Opne",

                           xaxis={'title': 'Date', 'showline': True, 'linecolor': 'black', "showspikes": True,
                                  'spikemode': 'across', "spikesnap": 'cursor', "spikethickness": 1,
                                  'spikedash': 'solid',
                                  "spikecolor": 'black',
                                  'linewidth': 2},
                           xaxis_showgrid=True,
                           xaxis_gridcolor='rgb(10,10,10)',

                           yaxis={'title': 'Price BTC (USD)', 'side': 'right', 'showline': True, 'linecolor': 'black',
                                  'linewidth': 2},
                           yaxis_type="log",
                           yaxis_showgrid=False,

                           legend_orientation="h",
                           plot_bgcolor='rgb(255,255,255)',
                           height=800)

        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph open'
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
            y.append(float(d.close))

        trace1 = go.Scatter(x=x, y=y, marker_color='rgba(255, 0, 0, .8)', mode="lines")

        data = go.Data([trace1])
        layout = go.Layout(title="Close", xaxis={'title': 'Date'}, yaxis={'title': 'Value'}, height=800)
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph close'
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
