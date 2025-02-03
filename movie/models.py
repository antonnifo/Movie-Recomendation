from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Movie(models.Model):
    title = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=200,
                      help_text='Should auto fill as you add title text')
    genres = models.CharField(max_length=200,  help_text='Add more than one separate using |')
    year = models.DateField()
    actors = models.CharField(max_length=250,help_text='Add more than one separate using |')
    director = models.CharField(max_length=250)
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_movies', blank=True, null=True)


    average_rating = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Average Rating',
        help_text='Average rating of the movie based on user reviews (0 indicates no ratings).'
    )   

    # Many-to-Many field for favouriting
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorite_movies',
        blank=True,
        help_text='Users who have marked this movie as a favorite.'
    )    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ('-updated',)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Rating choices from 1 to 5
class Rating(models.IntegerChoices):
    ONE = 1, '1'
    TWO = 2, '2'
    THREE = 3, '3'
    FOUR = 4, '4'
    FIVE = 5, '5'

class MovieReview(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='movie_reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveSmallIntegerField(
        choices=Rating.choices,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Rating',
        help_text='Rate the movie from 1 (worst) to 5 (best).'
    )
    review = models.TextField(
        max_length=1000,
        verbose_name='Review',
        help_text='Write your review here (maximum 1000 characters).'
    )
    is_active = models.BooleanField(default=True)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)     

    class Meta:
        ordering = ['-created']
        verbose_name = 'movie Review'
        verbose_name_plural = 'movie Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'user'], name='unique_user_movie_review')
        ]
        indexes = [
            models.Index(fields=['movie']),
            models.Index(fields=['user']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        # return f'{self.movie.title} - {self.user.username} ({self.rating}/5)'
        return f'({self.rating}/5) Review for {self.movie.title}'



@receiver(post_save, sender=MovieReview)
def update_movie_average_rating_on_save(sender, instance, **kwargs):
    """
    Update the average rating of the movie whenever a review is saved.
    """
    # Only consider active reviews
    active_reviews = instance.movie.movie_reviews.filter(is_active=True)
    aggregate = active_reviews.aggregate(average=models.Avg('rating'))
    average = aggregate['average'] or 0.0
    # Round to the nearest integer
    rounded_average = int(round(average))
    # Update the movie's average_rating
    instance.movie.average_rating = rounded_average
    instance.movie.save()


@receiver(post_delete, sender=MovieReview)
def update_movie_average_rating_on_delete(sender, instance, **kwargs):
    """
    Update the average rating of the movie whenever a review is deleted.
    """
    if not instance.is_active:
        # If the deleted review was inactive, no need to update
        return

    active_reviews = instance.movie.movie_reviews.filter(is_active=True)
    aggregate = active_reviews.aggregate(average=models.Avg('rating'))
    average = aggregate['average'] or 0.0
    # Round to the nearest integer
    rounded_average = int(round(average))
    # Update the movie's average_rating
    instance.movie.average_rating = rounded_average
    instance.movie.save()
