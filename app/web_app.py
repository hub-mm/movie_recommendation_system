# ./app/web_app.py
from main import main_func
from flask import Flask, redirect, url_for, request, render_template
import ast

app = Flask(__name__)


@app.route('/home')
def home():
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(4, amount=amount)
    return render_template('index.html', movies=movies)


@app.route('/rating')
def rating():
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(1, amount=amount)
    for movie in movies:
        genres = movie['genres']
        genres_string = ', '.join(genres)
        movie['genres'] = genres_string

        production_companies = movie['production_companies']
        production_companies_list = ast.literal_eval(production_companies)
        movie['production_companies'] = ', '.join([production['name'] for production in production_companies_list])

    return render_template('rating.html', movies=movies)


@app.route('/genre')
def genre():
    genre_val = request.args.get('genre', 'action').strip()
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(2, amount=amount, genre=genre_val)
    for movie in movies:
        production_companies = movie['production_companies']
        production_companies_list = ast.literal_eval(production_companies)
        movie['production_companies'] = ', '.join([production['name'] for production in production_companies_list])

    return render_template('genre.html', movies=movies)


@app.route('/similar')
def similar():
    title_val = request.args.get('title', 'The Godfather').strip().lower()
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(3, amount=amount, title=title_val)
    for movie in movies:
        genres = movie['genres']
        genres_string = ', '.join(genres)
        movie['genres'] = genres_string

        genres = movie['cast']
        genres_string = ', '.join(genres).title()
        movie['cast'] = genres_string

    return render_template('similar.html', movies=movies)


if __name__ == '__main__':
    app.run(port=8000, debug=False)