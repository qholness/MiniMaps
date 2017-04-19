from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from flask import request, session, redirect, url_for, abort, render_template, flash
import pandas as pd
import datetime
global timestamp
timestamp = lambda : datetime.datetime.strftime(datetime.datetime.utcnow(), "%D %T")


def checkUserNameIntegrity(username):
    # Some error checks...
    return username


def encodePassword(password):
    '''Hash and salt password'''
    t_sha = hashlib.sha512()
    password = str.encode(password)
    salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    t_sha.update(password + salt)
    hashedpassword = base64.urlsafe_b64encode(t_sha.digest())
    return hashedpassword




# def decodePassword(password):
#     t_sha = hashlib.sha512()
#     password = str.encode(password)
#     salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
#     t_sha.update(password + salt)
#     hashedpassword = base64.urlsafe_b64encode(t_sha.digest())
#     return hashedpassword


################ User Registration ################
@MinimalMaps.route('/register')
def register():
    if not session.get('logged_in'):
        db = get_db()
        leagues = list(pd.read_sql('''SELECT DISTINCT [name] FROM leagues''', db)['name'])
        db.close()
        flash("Enter your credentials to crete an account")
        return render_template('register.html', leagues=leagues)
    flash('You are already logged in', 'warning')
    return redirect(url_for('index'))


@MinimalMaps.route('/submit_reg', methods=['POST'])
def submitRegistration():
    # Registration confirmation...
    
    db = get_db()
    # password = encodePassword(request.form['password']) # hash password with salt
    username = request.form.get('username')
    password = request.form.get('password')
    league = request.form.get('leagueSelection')

    if not username:
        flash("Please enter a username", 'warning')
    
    if not password:
        flash("Please enter a password", 'warning')
    
    if not league:
        flash("Please select a league you'd like to join", 'warning')
        
    db.execute('''INSERT INTO users (username, [password], [league]) VALUES (?, ?, ?)''',
        (username, password, league)
    )
    db.close()
    flash('You have registered', 'success')
    return redirect(url_for('login'))


################ User Login ################
@MinimalMaps.route('/login')
def login():
    '''User login page'''
    return render_template('login.html')


@MinimalMaps.route('/execute-login', methods=['POST'])
def login_user():
    '''POST method for user login'''    
    db = get_db() # Establish database connection
    
    data = db.execute('''SELECT [username], [password] FROM users''') # Handle logins better please. I don't want to expose anything more than necessary...
    
    combo = data.fetchone() # Brute force check login
    while combo:
        username, password = combo

        # Form data
        checkname = request.form['username']
        checkpass = request.form['password']

        if checkname == username:
            if checkpass == password:
                session['logged_in'] = True
                session['user'] = checkname
                session['login_time'] = timestamp()
                flash('Logged in', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'warning')
        combo = data.fetchone()
    flash('Invalid username', 'warning')
    return redirect(url_for('login'))

@MinimalMaps.route('/logout')
def logout():
    '''Log user out'''
    session.pop('logged_in', None)
    session.pop('user', None)
    session.pop('login_time', None)

    flash('You were logged out', 'info')

    return redirect(url_for('index'))
