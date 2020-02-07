from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import GraphOpen, GraphClose, GraphHigh, index, about_us, graphs

urlpatterns = [
    path('', index, name='index'),
    path('graphs/', graphs, name='graphs'),
    path('about/', about_us, name='about_us'),
    path('graph_open/', GraphOpen.as_view(), name='graph_open'),
    path('graph_close/', GraphClose.as_view(), name='graph_close'),
    path('graph_high/', GraphHigh.as_view(), name='graph_high'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
