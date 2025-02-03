from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .apps import MovieConfig
from django.http import HttpResponseRedirect    


from django.contrib import messages
from .models import Movie, MovieReview
from .forms import MovieForm, MovieReviewForm

from . import helpers


def search_content_based(title: str, top_n=5) -> pd.DataFrame:
    """
    Searches for the most similar movie titles (content-based)
    using the TF-IDF matrix stored in MovieConfig.
    Returns top_n matching rows from MOVIES DataFrame.
    """
    from .helpers import clean_title

    if not title.strip():
        return pd.DataFrame()

    cleaned_query = clean_title(title)
    query_vec = MovieConfig.VECTORIZER.transform([cleaned_query])

    similarity = cosine_similarity(
        query_vec, MovieConfig.TFIDF_MATRIX).flatten()


    # Indices of top_n matches
    indices = np.argpartition(similarity, -top_n)[-top_n:]


    # Sort them by descending similarity
    best_indices = indices[np.argsort(-similarity[indices])]

    results = MovieConfig.MOVIES.iloc[best_indices].copy()
    results.reset_index(drop=True, inplace=True)
    return results


def find_similar_movies_item_based(movie_id: int, top_n=10) -> pd.DataFrame:
    """
    Given a raw movie_id from the content-based search, this function uses 
    Surprise's item-item KNN to find similar items. We use the official 
    `trainset.to_inner_iid()` and `trainset.to_raw_iid()` methods instead of 
    relying on _inner2raw_id_items.
    """
    algo = MovieConfig.RATING_ALGO
    if not algo:
        return pd.DataFrame()

    # 1) Convert the raw ID (int or str) to the Surprise "inner" ID
    #    Surprise might expect a string if its built-in loader sees item IDs as strings.
    #    If content_results returns an int, do str(movie_id):
    trainset = algo.trainset
    try:
        inner_id = trainset.to_inner_iid(
            str(movie_id))  # or str(movie_id) if needed
    except ValueError:
        # If that raw_id doesn't exist in the trainset, return empty
        return pd.DataFrame()

    # 2) Get the nearest neighbors in "inner" ID space
    neighbors = algo.get_neighbors(inner_id, k=top_n)


    # 3) Convert each neighbor from "inner" ID back to raw ID
    neighbor_raw_ids = [trainset.to_raw_iid(n) for n in neighbors]


    # 4) If your `movies_df["movieId"]` is int, convert neighbor_raw_ids to int
    neighbor_raw_ids = [int(rid) for rid in neighbor_raw_ids]

    # 5) Filter your MOVIES DataFrame
    movies_df = MovieConfig.MOVIES
    similar_movies = movies_df[movies_df["movieId"].isin(
        neighbor_raw_ids)].copy()
  
    return similar_movies

@login_required
def index(request: HttpRequest):
    """
    Home page: search form.
    """
    return render(request, 'site/index.html')



def search_results(request):
    query = request.POST.get('s', '').strip()
    recommended_movies = pd.DataFrame()

    if request.method == 'POST' and query:
        # 1. Content-based search (returns a df with columns including "movieId")
        content_results = search_content_based(query, top_n=5)

        if not content_results.empty:
            best_match_id = content_results.iloc[0]["movieId"]

            # 2. Item-based CF
            recommended_movies = find_similar_movies_item_based(
                best_match_id, top_n=10)
                
            # 3. Select only the desired columns
            recommended_movies = recommended_movies[[
                'title', 'release_date', 'IMDb_URL']]
        else:
            print("No content-based results for query:", query)


    context = {
        'query': query,
        'movies': recommended_movies,
    }
    return render(request, 'site/results.html', context)


def manage_movies(request):
    movies  = Movie.objects.prefetch_related('favorited_by').all()
    context = {
        'movies': movies,
    }
    return render(request, 'site/manage_movies.html', context)



def add_movie(request):

    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, f"You have added {\
                             movie} Thank you")
            return redirect('movie:manage_movies')
        else:
            messages.error(
                request, "There was an error with your submission. Please check the form and try again."
            )
    else:
        form = MovieForm()

    context = {
        'form': form,

    }
    return render(request, 'site/add_movie.html', context)



def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"You have successfully updated film {movie}.")
            return redirect('movie:manage_movies')
        else:
            # Add error message for clarity
            messages.error(
                request, "There was an error with your submission. Please check the form and correct any issues.")
    else:
        form = MovieForm(instance=movie)

    context = {
        'form': form,
        'movie': movie,
        }

    return render(request, 'site/add_movie.html', context)



def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        movie.delete()
        messages.info(request, f"You have deleted the film {movie}")
        return redirect('movie:manage_movies')

    return render(request, 'site/delete_movie.html', {'object': movie})




def manage_movie_ratings(request,pk):
    movie = get_object_or_404(Movie, pk=pk)
    ratings = movie.movie_reviews.filter(is_active=True)

    context = {
        'movie': movie,
        'ratings': ratings,
    }

    return render(request, 'site/ratings/manage_movie_ratings.html', context)



def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, f"You have rated the film {movie} Thank you")
            return redirect('movie:manage_movie_ratings', pk=pk)
        else:
            messages.error(
                request, "There was an error with your submission. Please check the form and try again."
            )
    else:
        form = MovieReviewForm()

    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'site/ratings/rate_movie.html', context)



def edit_movie_rating(request, pk):
    rating = get_object_or_404(MovieReview, pk=pk)
    movie = rating.movie

    if request.method == 'POST':
        form = MovieReviewForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"You have successfully updated rating for film {movie}.")
            return redirect('movie:manage_movie_ratings', pk=movie.pk)
        else:
            # Add error message for clarity
            messages.error(
                request, "There was an error with your submission. Please check the form and correct any issues.")
    else:
        form = MovieReviewForm(instance=rating)

    context = {
        'form': form,
        'movie': movie,
        'rating': rating
        }

    return render(request, 'site/ratings/rate_movie.html', context) 

def delete_movie_rating(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    movie = review.movie

    if request.method == "POST":
        review.delete()
        messages.info(request, f"You have deleted  your review for film {movie}")
        return redirect('movie:manage_movie_ratings', pk=movie.pk)

    return render(request, 'site/ratings/delete_rating.html', {'object': review})    

@login_required
def toggle_favorite(request, movie_pk):
    """
    Toggle the favorite status of a movie for the logged-in user.
    """
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if user in movie.favorited_by.all():
        movie.favorited_by.remove(user)
        messages.info(request, f"Removed '{movie.title}' from your favorites.")
    else:
        movie.favorited_by.add(user)
        messages.success(request, f"Added '{movie.title}' to your favorites.")

    # Redirect back to the page the user came from, if available.
    next_url = request.GET.get('next', None)
    if next_url:
        return redirect(next_url)
    else:
        # Fallback to a default view, e.g., the movie list page.
        return HttpResponseRedirect(reverse('movie:movie_list'))    