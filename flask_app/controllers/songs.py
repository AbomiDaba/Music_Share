from flask.globals import request, session
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.song import Song
from flask_app.models.user import User

@app.route('/add_page/song')
def add_song_page():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('create_song.html', user = User.get_one(data))

@app.route('/create/song', methods = ['POST'])
def create():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'artist': request.form['artist'],
        'name': request.form['name'],
        'genre': request.form['genre'],
        'user_id': session['user_id']
    }
    if not Song.validate_songs(request.form):
        return redirect('/add_page/song')
    Song.create_song(data)
    return redirect('/dashboard')

@app.route('/edit_page/song/<int:song_id>')
def edit_song(song_id):
    if 'user_id' not in session:
        return redirect ('/')
    song_data = {
        'id' : song_id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('edit_song.html', user = User.get_one(user_data), song = Song.get_one_song(song_data))

@app.route('/edit/song/<int:song_id>', methods = ['POST'])
def edit(song_id):
    if 'user_id' not in session:
        return redirect ('/')
    data ={
        'id' : song_id,
        'artist': request.form['artist'],
        'name': request.form['name'],
        'genre': request.form['genre'],
    }
    Song.edit_song(data)
    return redirect('/dashboard')

@app.route('/like/song/<int:song_id>', methods = ['POST'])
def create_like(song_id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'FK_likes_users' : session['user_id'],
        'song_id': song_id
    }
    Song.create_like(data)
    return redirect('/dashboard')

@app.route('/destroy/song/<int:song_id>')
def destroy_song(song_id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : song_id
    }
    Song.destroy_song(data)
    return redirect('/dashboard')

@app.route('/destroy/like/<int:song_id>')
def destroy_like(song_id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'song_id' : song_id,
        'FK_likes_users' : session['user_id']
    }

    Song.destroy_like(data)
    return redirect('/dashboard')

