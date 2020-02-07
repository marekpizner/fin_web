from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic import TemplateView

import plotly.offline as opy
import plotly.graph_objs as go

from .models import Olhc

list_of_graphs = [
    {
        'title': 'Open',
        'url': 'graph_open'
    },
    {
        'title': 'Close',
        'url': 'graph_close'
    },
    {
        'title': 'High',
        'url': 'graph_high'
    }
]


def index(request):
    context = {
        'graphs': list_of_graphs
    }

    return render(request, 'fin_web_graphs/index.html', context)


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

        trace1 = go.Scatter(x=x, y=y, mode="lines")

        data = go.Data([trace1])
        layout = go.Layout(title="Opne", xaxis={'title': 'Date'}, yaxis={'title': 'Value'}, height=800)
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

        trace1 = go.Scatter(x=x, y=y, mode="lines")

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

        trace1 = go.Scatter(x=x, y=y, mode="lines")

        data = go.Data([trace1])
        layout = go.Layout(title="High", xaxis={'title': 'Date'}, yaxis={'title': 'Value'}, height=800)
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph high'
        return context
