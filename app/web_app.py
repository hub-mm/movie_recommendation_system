# ./app/web_app.py
from main import main_func
from scripts.script_app.script_users import User
from config import SECRET_KEY_MOVIES
from flask import Flask, request, render_template, redirect, url_for, session, flash
import ast
import validators


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


# @app.route('/user_page')
@app.route('/user_page/<name>')
def user_page(name=None):
    session_username = session.get('username')
    return render_template('user_page.html', name=session_username)

@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)