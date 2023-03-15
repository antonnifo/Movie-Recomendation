from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200,
                    unique=True,  help_text='Should auto fill as you add title text')
    genres = models.CharField(max_length=200,  help_text='Add more than one separate using |')
    year = models.DateField()
    actors = models.CharField(max_length=250,help_text='Add more than one separate using |')
    director = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title
