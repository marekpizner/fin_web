from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import GraphMovingAverage, GraphWeekMovingAverage, GraphStockToFlow, index, about_us, graphs

urlpatterns = [
    path('', index, name='home'),
    path('graphs/', graphs, name='graphs'),
    path('about/', about_us, name='about_us'),

    path('graph_moving_average/', GraphMovingAverage.as_view(), name='graph_moving_average'),
    path('graph_week_moving_average/', GraphWeekMovingAverage.as_view(), name='graph_week_moving_average'),
    path('graph_stock_to_flow/', GraphStockToFlow.as_view(), name='graph_stock_to_flow'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
