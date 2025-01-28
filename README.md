
# Movie-Recommendation [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

A movie recommendation system built with Django, Pandas, and the Surprise library.

This project demonstrates a hybrid approach to recommending movies:
1. **Content-Based Filtering** (TF-IDF on movie titles).
2. **Collaborative Filtering** (item-based KNN using the Surprise library’s built-in MovieLens dataset).

## Table of Contents
1. [How It Works](#how-it-works)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Setup Instructions](#setup-instructions)
   - [Linux](#linux)
   - [Windows](#windows)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [License](#license)

## How It Works

### 1. Data Loading
- We load or download the MovieLens-100k dataset through the Surprise library.
- For content-based search, we also parse the `u.item` file (or CSV files) to retrieve movie metadata (e.g., titles, genres).

### 2. Content-Based Filtering (TF-IDF)
- Each movie title is “cleaned” (lowercased, punctuation removed) and transformed into a TF-IDF vector.
- When a user searches for a movie, we transform the search query into the same TF-IDF space and calculate cosine similarity.
- We pick the top matching titles from the dataset (e.g., the top 5).

### 3. Collaborative Filtering (Surprise)
- We train an item-based KNN model using user ratings from MovieLens.
- Once we identify a “best match” movie from the content-based step, we retrieve its nearest neighbor movies based on item-item similarity scores from Surprise.
- The final list of recommended movies is then displayed to the user.

### 4. Django Integration
- We utilize Django views to handle search queries, perform the ML logic, and render results in templates.
- On the backend, we load the models at application startup (via `apps.py`) so subsequent requests are fast.

## Project Structure

A simplified overview:

```
Movie-Recommendation/
├─ movie/
│  ├─ apps.py            # AppConfig - loads data/models on startup
│  ├─ views.py           # Django views for search & recommendation
│  ├─ templates/
│  │  └─ site/
│  │     ├─ index.html
│  │     └─ results.html
│  ├─ helpers.py         # Helper functions (e.g., cleaning titles)
│  ├─ data/              # CSV files or additional data if needed
├─ requirements.txt      # Dependencies
├─ manage.py             # Django entry point
└─ README.md
```

## Requirements
1. **Python 3.7+** (or higher).
2. **Django 3.2+** (or the version specified in your `requirements.txt`).
3. **Pandas**, **scikit-surprise**, and any other libraries listed in `requirements.txt`.
4. A modern web browser to access the application once it is running.

## Setup Instructions

### Linux
1. **Clone the repository:**
    ```bash
    git clone git@github.com:antonnifo/Movie-Recomendation.git
    cd Movie-Recomendation
    ```

2. **Create a virtual environment** (optional, but recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **(Optional)** Download additional data and place CSV files in `movie/data/` (if you’re using local data rather than Surprise’s built-in datasets).

5. **Run database migrations** (if using Django models for sessions or user authentication):
    ```bash
    python manage.py migrate
    ```

6. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Open your browser** at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the app.

### Windows
1. **Clone or download the repository.**

2. **Open Command Prompt or PowerShell** and navigate into the project directory:
    ```powershell
    cd Movie-Recomendation
    ```

3. **Create a virtual environment:**
    ```powershell
    python -m venv .venv
    .venv\Scriptsctivate
    ```

4. **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

5. **(Optional)** Download data and place in `movie/data/` if needed.

6. **Migrate** (if required):
    ```powershell
    python manage.py migrate
    ```

7. **Run the Django development server:**
    ```powershell
    python manage.py runserver
    ```

8. **Visit** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
1. **Navigate to the home page** (`index.html`).
2. **Enter a movie title or keyword** in the search form.
3. **Submit** to see:
   - Top content-based match for the query.
   - Similar movies recommended by the collaborative filtering model.
4. **Explore the results table** and see if the recommendations match your preferences.

## Troubleshooting
- **No Recommendations Found**
  - Ensure that the search query matches at least one movie in the dataset.
  - Check if the dataset (MovieLens or local CSV) actually contains the movie you’re searching for.

- **Import/Version Errors**
  - Make sure you’re using the same Python version for creating the virtual environment and installing dependencies.
  - Downgrade to a NumPy 1.x version if you run into `numpy.core.multiarray` or other ABI mismatch issues with scikit-surprise.

- **Performance**
  - The built-in dataset is fine for demos. For larger datasets, consider caching or a production database.

## License

This project is provided under the **MIT License**. Feel free to modify and adapt it for your own needs.

---

**Enjoy exploring and improving this Movie Recommendation System!**
