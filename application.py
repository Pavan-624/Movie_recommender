import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a25f47f5f2292e412a50d8713089b9f8&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')  # Use .get() method to safely get the value
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Select Movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Filter out None values from posters list
    valid_posters = [poster for poster in posters if poster is not None]

    # Display recommended movies and posters
    for name, poster in zip(names[:len(valid_posters)], valid_posters):
        st.text(name)
        st.image(poster,width=200)
