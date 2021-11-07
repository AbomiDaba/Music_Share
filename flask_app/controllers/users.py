from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.song import Song
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = 'iringvneii;ai;jfngri;albjdbd niueeuhrfiuohfr'
@app.route('/')
def index():
    return redirect('/register_login')

@app.route('/register_login')
def main_page():
    return render_template('reg_login.html')



@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invlid email or password','login')
        return redirect('/')

    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def login_page():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }

    return render_template('dashboard.html', liked_song_id_list = Song.get_liked_songs(data), user = User.get_one(data), songs=Song.get_songs_with_users_and_likers())

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')