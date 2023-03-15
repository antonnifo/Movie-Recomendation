from django.contrib import admin
from  .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = ('title', 'genres', 'year', 'actors', 'director', 'created', 'updated')
    search_fields = ('title', 'actors', 'director')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy      = 'updated'
    list_per_page       = 10    
