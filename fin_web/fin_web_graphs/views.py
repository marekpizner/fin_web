import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as opy
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound

from .graphs.moving_average import MovingAverage
from .graphs.weekly_moving_average import WeeklyMovingAverage
from .graphs.stock_to_flow import StockToFlow
from .graphs.rsi import RSI
from .graphs.mining_diff import MiningDiff
from .models import Olhc

graphs_list = [
    MovingAverage(None, None, None),
    WeeklyMovingAverage(None),
    StockToFlow(None),
    RSI(None),
    MiningDiff()
]

list_of_graphs = []

for g in graphs_list:
    config = g.get_config()

    list_of_graphs.append(config)


def index(request):
    context = {}
    return render(request, 'fin_web_graphs/index.html', context)


def graphs(request):
    context = {
        'graphs': list_of_graphs
    }

    return render(request, 'fin_web_graphs/graphs.html', context)


def about_us(request):
    context = {}
    return render(request, 'fin_web_graphs/about.html', context)


def graph_general(request, graph_id):
    template_name = 'fin_web_graphs/graph.html'

    if graph_id == 'graph_moving_average':
        graph = MovingAverage(365 * 2, 365 * 2)
    elif graph_id == 'graph_week_moving_average':
        graph = WeeklyMovingAverage(200 * 7)
    elif graph_id == 'graph_stock_to_flow':
        graph = StockToFlow(200 * 7)
    elif graph_id == 'rsi':
        graph = RSI(14)
    elif graph_id == 'mining_difficulty':
        graph = MiningDiff()
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    context = {}
    _, context = graph.get_plot(context)

    return render(request, template_name, context)
