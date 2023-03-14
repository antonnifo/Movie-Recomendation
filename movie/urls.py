from django.urls import path
# from django.views.generic import TemplateView
from . import views

app_name = 'movie'

urlpatterns = [
     # path('', TemplateView.as_view(template_name="site/index.html"), name='home'),
     path('', views.index, name='home'),
     path('results/', views.search_results, name='search'),
]