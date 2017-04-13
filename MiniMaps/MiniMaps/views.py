from __init__ import MinimalMaps
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from dbtools import *
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
    if session.get('logged_in'):
        return redirect(url_for('test'))
    return render_template('register.html')


@MinimalMaps.route('/testpost')
def test():
    if not session.get('logged_in'):
        abort(401)
    return render_template('test.html')


@MinimalMaps.route('/login', methods=['GET', 'POST'])
def login():
    '''User login page'''
    error = None
    db = get_db() # Establish database connection
    
    data = pd.read_sql('''SELECT username, [password] FROM users''', db)
    data = {k : v for k,v in zip(data.username, data.password)}

    if request.method == 'POST':
        key = data.get(request.form['username'])
        if not key:
            error = 'Invalid username'
        elif request.form['password'] != key:
            error = 'Wrong password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)


@MinimalMaps.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))