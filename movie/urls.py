from django.urls import path
# from django.views.generic import TemplateView
from . import views

app_name = 'movie'

urlpatterns = [
     # path('', TemplateView.as_view(template_name="site/index.html"), name='home'),
     path('', views.dashboard, name="dashboard"),
     path('search/', views.index, name='home'),
     path('results/', views.search_results, name='search'),
     path('movies/', views.manage_movies, name='manage_movies'),
     path('movies/add/', views.add_movie, name='add_movies'),
     path('movies/<int:pk>/update/', views.edit_movie, name='edit_movies'),
     path('movies/<int:pk>/delete/', views.delete_movie, name='delete_movies'),


     path('movies/<int:pk>/ratings', views.manage_movie_ratings, name='manage_movie_ratings'),
     path('movies/<int:pk>/ratings/add/', views.rate_movie, name='rate_movie'),
     path('movies/ratings/<int:pk>/edit/', views.edit_movie_rating, name='edit_rate_movie'),
     path('movies/ratings/<int:pk>/delete/', views.delete_movie_rating, name='delete_rate_movie'),

      path('favorite-toggle/<int:movie_pk>/', views.toggle_favorite, name='favorite_toggle'),
]