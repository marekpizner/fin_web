from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, about_us, graphs, graph_general

urlpatterns = [
                  path('', index, name='home'),
                  path('graphs/', graphs, name='graphs'),
                  path('about/', about_us, name='about_us'),

                  path(r'graph/<slug:graph_id>/', graph_general, name='graph_general'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
