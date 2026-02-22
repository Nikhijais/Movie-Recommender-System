from flask import Flask, render_template, request
import pickle
import pandas as pd

import os
import gdown

# Download similarity.pkl if not present
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=1eiNSchaa4QM4dPIUzy_lL0o8wtM2m_7H"
    gdown.download(url, "similarity.pkl", quiet=False)

app = Flask(__name__)

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

@app.route('/', methods=['GET','POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommendations = recommend(selected_movie)

    return render_template('index.html',
                           movie_list=movies['title'].values,
                           recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)