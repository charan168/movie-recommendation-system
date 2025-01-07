import pickle
import streamlit as st
import requests
import pandas as pd

# Function to fetch the poster image of a movie using TheMovieDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Streamlit header
st.header('Movie Recommender System')

# Load pickled data
try:
    # Load the movie DataFrame
    with open('model/movie_list.pkl', 'rb') as file:
        movies = pickle.load(file)

    # Load the similarity matrix
    with open('model/similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)

    # Ensure `movies` is a DataFrame
    if not isinstance(movies, pd.DataFrame):
        raise ValueError("The loaded 'movies' object is not a DataFrame.")

except FileNotFoundError:
    st.error("Pickle files not found. Ensure 'movie_list.pkl' and 'similarity.pkl' exist in the 'model' directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Display recommendations on button click
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)  # Create 5 columns for displaying recommendations
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
