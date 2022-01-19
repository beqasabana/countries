from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('index.html', active_user=active_user)
    return render_template('index.html')

@app.route('/register')
def register_view(updating = False):
    if 'user' in session and not updating:
        return redirect('/')
    return render_template('register.html')

@app.route('/edit/profile')
def update_profile():
    if 'user' not in session:
        return redirect('/')
    return register_view(True)

@app.route('/login')
def login_view():
    if 'user' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/profile/<string:name>/<int:id>')
def dashboard(name, id):
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('profile.html', active_user=active_user)
    else:
        flash("You are not logged in!", 'not-loggedin')
        return redirect('/')

@app.route('/register/user', methods=['POST'])
def register_user():
    if not User.validate_registation(request.form):
        return redirect('/register')
    print(request.form)
    data = {
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'], 
        'email': request.form['email'], 
        'password': bcrypt.generate_password_hash(request.form['password']),
        'info': request.form['info']
    }
    session['user'] = User.create(data)
    return redirect('/')

@app.route('/login/validation', methods=['POST'])
def login():
    if User.validate_login(request.form):
        session['user'] = User.validate_login(request.form)
        return redirect('/')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')