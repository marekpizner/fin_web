from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic import TemplateView

import plotly.offline as opy
import plotly.graph_objs as go

from .models import Olhc

list_of_graphs = [
    {
        'title': 'graph_open'
    },
    {
       'title': 'graph_close'
    },
    {
        'title': 'graph_high'
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
            y.append(d.open)
            print(x)
        # x = data['open']
        # y = data['date']
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = go.Layout(title="Meine Daten", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph open'
        return context


class GraphClose(TemplateView):
    template_name = 'fin_web_graphs/graph.html'

    def get_context_data(self, **kwargs):
        context = super(GraphClose, self).get_context_data(**kwargs)

        x = [-2, 0, 4, 6, 7]
        y = [q ** 2 - q + 3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = go.Layout(title="Meine Daten", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph close'
        return context


class GraphHigh(TemplateView):
    template_name = 'fin_web_graphs/graph.html'

    def get_context_data(self, **kwargs):
        context = super(GraphHigh, self).get_context_data(**kwargs)

        x = [-2, 0, 4, 6, 7]
        y = [q ** 2 - q + 3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = go.Layout(title="Meine Daten", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div
        context['title'] = 'Graph high'
        return context
