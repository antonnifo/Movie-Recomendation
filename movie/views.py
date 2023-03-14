from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.decorators import login_required

from sklearn.feature_extraction.text import TfidfVectorizer

from . import helpers

MOVIES = pd.read_csv("movie/data/movies.csv")
RATINGS = pd.read_csv("movie/data/ratings.csv") 


MOVIES["clean_title"] = MOVIES["title"].apply(helpers.clean_title)

vectorizer = TfidfVectorizer(ngram_range=(1,2))
TFIDF = vectorizer.fit_transform(MOVIES["clean_title"]) 


def search(title):
    title = helpers.clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, TFIDF).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = MOVIES.iloc[indices].iloc[::-1] 

    return results 


def find_similar_movies(movie_id):
    similar_users = RATINGS[(RATINGS["movieId"] == movie_id) & (RATINGS["rating"] > 4)]["userId"].unique()
    similar_user_recs = RATINGS[(RATINGS["userId"].isin(similar_users)) & (RATINGS["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = RATINGS[(RATINGS["movieId"].isin(similar_user_recs.index)) & (RATINGS["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)

    return rec_percentages.head(10).merge(MOVIES, left_index=True, right_on="movieId")[["title", "genres"]]    

@login_required
def index(request): 
    return render (request, 'site/index.html' ,{}) 

def search_results(request):

    query = None
    similar_movies = None
    if request.method == 'POST':
        query = request.POST['s']

        results = search(query)
        movie_id = results.iloc[0]["movieId"]
        similar_movies = find_similar_movies(movie_id)
        

    context = {
                'query' : query,
                'movies': similar_movies,
              }
 
    return render (request, 'site/results.html' ,context)    