from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from flask import request, session, redirect, url_for, abort, render_template, flash
import pandas as pd
import hashlib
import base64
import uuid





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


@MinimalMaps.route('/submit_reg', methods=['POST'])
def submitRegistration():
    # Registration confirmation...
    
    
    # db = get_db()
    # password = encodePassword(request.form['password']) # hash password with salt
    # db.execute('''INSERT INTO users (username, [password]) VALUES (?, ?)''',
    #     [request.form['username'], password])
    # db.commit()
    flash('You have registered')
    return redirect(url_for('login'))



@MinimalMaps.route('/register', methods=['POST', 'GET'])
def register():
    if not session.get('logged_in'):
        flash("Enter your credentials to crete an account")
        return render_template('register.html')
    else:
        return redirect(url_for('index'))


@MinimalMaps.route('/test')
def test():
    if not session.get('logged_in'):
        # abort(401)
        return redirect(url_for('register'))
    return render_template('index.html')


@MinimalMaps.route('/login', methods=['GET', 'POST'])
def login():
    '''User login page'''
    error = None
    username, password = None, None
    combo = None
    db = get_db() # Establish database connection
    
    data = db.execute('''SELECT username, [password] FROM users''') # Handle logins better please. I don't want to expose anything more than necessary...
    

    if request.method == 'POST':
        combo = data.fetchone() # Brute force check login
        while combo:
            username, password = combo
            checkname = request.form['username']
            checkpass = request.form['password']
            if checkname == username:
                if checkpass == password:
                    session['logged_in'] = True
                    flash('Logged in')
                    return redirect(url_for('index'))
                else:
                    error = 'Incorrect password'
            combo = data.fetchone()
        error = 'Invalid username'

    return render_template('login.html', error=error)


@MinimalMaps.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))