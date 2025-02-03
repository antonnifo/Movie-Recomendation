from django import forms
from django.contrib.auth.models import User
from .models import Movie, MovieReview

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'genres',
            'year',
            'actors',
            'director',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter movie title'}),
            'genres': forms.TextInput(attrs={'placeholder': 'Add more than one, separated using |'}),
            'year': forms.DateInput(attrs={'type': 'date'}),
            'actors': forms.TextInput(attrs={'placeholder': 'Add more than one, separated using |'}),
            'director': forms.TextInput(attrs={'placeholder': 'Enter director name'}),
            'average_rating': forms.NumberInput(attrs={
                'min': 0,
                'max': 5,
                'placeholder': 'Enter average rating (0-5)'
            }),

        }
        labels = {
            'title': 'Movie Title',
            'genres': 'Genres',
            'year': 'Release Year',
            'actors': 'Actors',
            'director': 'Director',

        }
        help_texts = {
            'genres': 'Add more than one, separated using |',
            'actors': 'Add more than one, separated using |',
        }

class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']
        widgets = {

            'rating': forms.Select(attrs={'data-select2-selector': 'default'}),
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here (max 1000 characters)'}),
        }
        labels = {
           
            'rating': 'Your Rating',
            'review': 'Your Review',
        }
        help_texts = {
            'rating': 'Rate the movie from 1 (worst) to 5 (best).',
            'review': 'Write your review here (maximum 1000 characters).',
        }        