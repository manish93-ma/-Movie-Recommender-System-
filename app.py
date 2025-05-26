import streamlit as st
import pickle
import pandas as pd
import requests

TMDB_API_KEY = "0a7e8bce9c324cbde62410e3eaeee4e4"


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id  
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Choose a movie you like:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    st.subheader("Recommended Movies for You:")
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_container_width=True)

            st.caption(name)