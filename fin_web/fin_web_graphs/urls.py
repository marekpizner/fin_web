from django.urls import path

from .views import GraphOpen, GraphClose, GraphHigh, index

urlpatterns = [
    path('', index, name='index'),
    path('about/', index, name='about'),
    path('graph_open/', GraphOpen.as_view(), name='graph_open'),
    path('graph_close/', GraphClose.as_view(), name='graph_close'),
    path('graph_high/', GraphHigh.as_view(), name='graph_high')
]
