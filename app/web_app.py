# ./app/web_app.py
from main import main_func
from scripts.script_app.script_users import User
from config import SECRET_KEY_MOVIES
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import ast
import validators
import pickle
import json
import re


app = Flask(__name__)
app.secret_key = SECRET_KEY_MOVIES

@app.route('/home')
@app.route('/home/<name>')
def home(name=None):
    session_username = session.get('username')
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(4, amount=amount)

    if not name and session_username:
        return redirect(url_for('home', movies=movies, name=session_username, amount=amount))

    return render_template('index.html', movies=movies, name=name)


@app.route('/rating')
@app.route('/rating/<name>')
def rating(name=None):
    session_username = session.get('username')
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(1, amount=amount)
    for movie in movies:
        genres = movie.get('genres')
        movie['genres'] = ', '.join(genres)

        production_companies = movie.get('production_companies')
        production_companies_list = ast.literal_eval(production_companies)
        movie['production_companies'] = ', '.join([production['name'] for production in production_companies_list])

    if not name and session_username:
        return redirect(url_for(
            'rating',
            movies=movies,
            name=session_username,
            amount=amount
        ))

    return render_template(
        'rating.html',
        movies=movies,
        name=name,
        amount=amount
    )


@app.route('/genre')
@app.route('/genre/<name>')
def genre(name=None):
    session_username = session.get('username')
    genre_val = request.args.get('genre', 'action').strip()
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(2, amount=amount, genre=genre_val)
    for movie in movies:
        production_companies = movie.get('production_companies')
        production_companies_list = ast.literal_eval(production_companies)
        movie['production_companies'] = ', '.join([production['name'] for production in production_companies_list])

    if not name and session_username:
        return redirect(url_for(
            'genre',
            movies=movies,
            name=session_username,
            genre=genre_val,
            amount=amount
        ))

    return render_template(
        'genre.html',
        movies=movies,
        name=name,
        genre=genre_val,
        amount=amount
    )


@app.route('/similar')
@app.route('/similar/<name>')
def similar(name=None):
    session_username = session.get('username')
    title_val = request.args.get('title', 'The Godfather').strip().lower()
    amount = request.args.get('amount', 10, type=int)
    movies = main_func(3, amount=amount, title=title_val)
    for movie in movies:
        genres = movie.get('genres')
        movie['genres'] = ', '.join(genres)

        genres = movie.get('cast')
        movie['cast'] = ', '.join(genres).title()

    if not name and session_username:
        return redirect(url_for(
            'similar',
            movies=movies,
            name=session_username,
            title=title_val,
            amount=amount
        ))

    return render_template(
        'similar.html',
        movies=movies,
        name=name,
        title=title_val,
        amount=amount
    )


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        try:
            user = User.authenticate(username, password)

            session['user_id'] = user.user_id
            session['username'] = user.username

            flash('sign in successful!', 'success')
            return redirect(url_for(f"home"))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('sign_in.html')


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not email or not username or not password:
            flash('All fields are required.', 'danger')
            return render_template('new_user.html')

        if not validators.email(email):
            flash('Invalid email address. Please enter a valid one.', 'danger')
            return render_template('new_user.html')

        try:
            user = User.create_user(email, username, password)
            flash('User created successfully. Please sign in.', 'success')
            return redirect(url_for('sign_in'))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('new_user.html')


@app.route('/user_page/<name>')
def user_page(name=None):
    session_username = session.get('username')
    if not session_username:
        flash('You must be signed in to view your user page.', 'danger')
        return redirect(url_for('sign_in'))

    if session_username != name:
        flash('Access denied. You can only view your own user page.', 'danger')
        return redirect(url_for('home'))

    try:
        user = User.get_user(session_username)
        favourites = user.favourites
        return render_template('user_page.html', name=session_username, favourites=favourites)
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))

@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_favourite', methods=['POST'])
def add_favourite():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    username = session['username']

    raw_movie = request.json.get('movie')
    print(f"Raw movie type: {type(raw_movie)}, value: {raw_movie}")

    if not raw_movie:
        return jsonify({'error': 'No movie data provided.'}), 400

    try:
        if isinstance(raw_movie, dict):
            movie = raw_movie
        elif isinstance(raw_movie, str):
            raw_movie = raw_movie.replace("'", "\"")

            raw_movie = re.sub(r'datetime\.date\((\d+), (\d+), (\d+)\)', r'"\1-\2-\3"', raw_movie)

            movie = json.loads(raw_movie)
        else:
            raise ValueError('Movie data is in an unsupported format.')

        if not isinstance(movie, dict):
            raise ValueError('Parsed movie data is not a dictionary.')

    except (ValueError, json.JSONDecodeError, SyntaxError) as e:
        print(f"Error: {e}")
        print(f"Raw movie type: {type(raw_movie)}, value: {raw_movie}")
        return jsonify({'error': 'Invalid movie data format.'}), 400

    print(f"Processed movie: {movie}")
    print(f"Movie type: {type(movie)}")

    try:
        user = User.get_user(username)
        message = user.add_favourite(movie)
        return jsonify({'message': message, 'favourites': user.favourites}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/remove_favourite', methods=['POST'])
def remove_favourite():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    username = session['username']

    movie_title = request.json.get('title')

    if not movie_title:
        return jsonify({'error': 'No movie title provided.'}), 400

    try:
        user = User.get_user(username)
        message = user.remove_favourite(movie_title)
        return jsonify({'message': message, 'favourites': user.favourites}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def get_movie_info(title):
    file_path = './data/user_built/preprocessed_df.pkl'
    with open(file_path, 'rb') as f:
        movie_data = pickle.load(f)

    return movie_data.get(title, None)

if __name__ == '__main__':
    app.run(port=8000, debug=False)