import pickle
import streamlit as st
import requests
import pandas as pd

#H1guK4mXWPhuYut
# Function to fetch movie poster

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


# Recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        return [(movies.iloc[i[0]].title, fetch_poster(movies.iloc[i[0]].movie_id)) for i in distances[1:6]]
    except:
        return []


# Streamlit App UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("""<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommender System 🍿</h1>""",
            unsafe_allow_html=True)

# Load pickled data
try:
    with open('model/movie_list.pkl', 'rb') as file:
        movies = pickle.load(file)
    with open('model/similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
    if not isinstance(movies, pd.DataFrame):
        raise ValueError("Movies data is corrupted.")
except FileNotFoundError:
    st.error("Missing files: Ensure 'movie_list.pkl' and 'similarity.pkl' exist.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Movie search input
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list, index=0)

# Show recommendations
if st.button("🔍 Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend(selected_movie)

    if recommendations:
        st.subheader("✨ Recommended Movies for You")
        cols = st.columns(5)
        for col, (name, poster) in zip(cols, recommendations):
            with col:
                st.image(poster, width=150)
                st.write(f"**{name}**")
    else:
        st.error("No recommendations found. Try another movie!")

# Footer with Project Credits
st.markdown("""
    <div style='background-color: #2E2E2E; padding: 10px; border-radius: 10px; text-align: center; color: white; margin-top: 20px;'>
        <p style='font-size: 14px;'>ID: 2200039018</p>
    </div>
""", unsafe_allow_html=True)
