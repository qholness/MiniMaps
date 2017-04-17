from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from flask import request, session, redirect, url_for, abort, render_template, flash
import pandas as pd
import datetime
import hashlib
import base64
import uuid
global today
today = lambda : datetime.datetime.strftime(datetime.datetime.now(), "%D %T")






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




@MinimalMaps.route('/')
def index():
    
    return render_template('index.html')

################ User Registration ################
@MinimalMaps.route('/register')
def register():
    if not session.get('logged_in'):
        flash("Enter your credentials to crete an account")
        return render_template('register.html')
    
    else:
        
        return redirect(url_for('index'))


@MinimalMaps.route('/submit_reg', methods=['POST'])
def submitRegistration():
    # Registration confirmation...
    
    
    db = get_db()
    # password = encodePassword(request.form['password']) # hash password with salt
    db.execute('''INSERT INTO users (username, [password]) VALUES (?, ?)''',
        [request.form['username'], password])
    db.commit()
    flash('You have registered')
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
                session['login_time'] = today()
                flash('Logged in')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password')
        combo = data.fetchone()
    flash('Invalid username')
    return redirect(url_for('login'))

@MinimalMaps.route('/logout')
def logout():
    '''Log user out'''
    session.pop('logged_in', None)
    session.pop('user', None)
    session.pop('login_time', None)

    flash('You were logged out')

    return redirect(url_for('index'))

################ User views ################
@MinimalMaps.route('/me')
def showMe():
    '''User homepage'''
    if not session.get('user', None):
    
        flash("You must be logged in to view this page")
    
        return redirect(url_for('login'))
    
    db = get_db()
    row_zero = lambda data: {k : v[0] for k, v in data.items()}

    user_data = row_zero(
        pd.read_sql('''
            SELECT * 
            FROM users 
            WHERE [username] = '{}';'''
            .format(session['user']), db)
        .to_dict('list')
    )

    league_data = row_zero(
        pd.read_sql('''
            SELECT * 
            FROM leagues 
            WHERE [name] = '{}';'''
            .format(user_data['league']), db)
        .to_dict('list')
    )
    
    db.close()

    return render_template('me.html', user_data=user_data, league_data=league_data)

################ User views ################
@MinimalMaps.route('/game')
def game():
    
    return render_template('game.html')



