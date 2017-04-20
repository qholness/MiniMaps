'''
    Login views
'''

from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from MiniMaps.utils import *
from flask import request, session, redirect, url_for, abort, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import datetime


################ User Registration ################
@MinimalMaps.route('/register')
def register():
    if not session.get('logged_in'):
        db = get_db()
        leagues = list(pd.read_sql('''SELECT DISTINCT [name] FROM leagues''', db)['name'])
        db.close()
        flash("Enter your credentials to create an account", "info")
        return render_template('register.html', leagues=leagues)
    flash('You are already logged in', 'info')
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
        return redirect(url_for('register'))
    
    if not password:
        flash("Please enter a password", 'warning')
        return redirect(url_for('register'))

    if not league:
        flash("Please select a league you'd like to join", 'warning')
        return redirect(url_for('register'))
    
    try:
        db.execute('''INSERT INTO users (username, [password], [league]) VALUES (?, ?, ?)''',
            (username, generate_password_hash(password), league)
        )
    except:
        db.close()
        flash("Registration failed", "danger")
        return redirect(url_for('register'))

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
            if check_password_hash(password, checkpass):
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
    session.clear()
    flash('You were logged out', 'info')
    return redirect(url_for('index'))


@MinimalMaps.before_request
def timout_session_update():
    '''Remove user after 3 days of inactivity'''
    MinimalMaps.permanent_session_lifetime = datetime.timedelta(days=3)