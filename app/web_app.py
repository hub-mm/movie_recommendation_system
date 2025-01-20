# ./app/web_app.py
from main import main_func
from flask import Flask, redirect, url_for, request, render_template


app = Flask(__name__)

@app.route('/home')
def home():
    movies = main_func(5, amount=20)
    return render_template('index.html', movies=movies)

@app.route('/rating')
def rating():
    movies = main_func(1, amount=20)
    return render_template('rating.html', movies=movies)

@app.route('/genre')
def genre():
    genre_val = request.args.get('genre', 'action').strip()
    movies = main_func(2, amount=20, genre=genre_val)

    return render_template('genre.html', movies=movies)

@app.route('/similar')
def similar():
    title_val = request.args.get('title', 'The Godfather').strip().lower()
    movies = main_func(4, amount=20, title=title_val)

    return render_template('similar.html', movies=movies)

if __name__ == '__main__':
    app.run(port=8000, debug=True)