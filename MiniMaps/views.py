from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from flask import request, session, redirect, url_for, abort, render_template, flash
import pandas as pd
import hashlib
import base64
import uuid




def check_login_status(redirect_url='login'):
    '''Check to see if a user is logged in'''
    if not session.get('logged_in'):
        
        flash('You must be logged in to view this page')
        return redirect(url_for(redirect_url))


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


@MinimalMaps.route('/client_statuses')
def client_statuses():
    check_login_status()
    db = get_db()
    data = pd.read_sql("SELECT [name], [status], [instance_url], [import_url] FROM clients", db)
    db.close()
    return render_template('client_statuses.html', data=data)


@MinimalMaps.route('/submit_sql')
def submit_sql():
    check_login_status()
    return render_template('submit_sql.html')


@MinimalMaps.route('/execute', methods=['POST'])
def execute_sql():
    check_login_status()
    statements = request.form['sql']
    statements = statements.split(';')

    db = get_db()
    for s in statements:
        db.execute(s)
        flash(s)
    db.close()
    return redirect(url_for('index'))


@MinimalMaps.route('/client_form', methods=['GET'])
def submit_client_form():
    '''Form for submitting a new client'''
    check_login_status()
    return render_template('submit_new_client.html')


@MinimalMaps.route('/submit_client', methods=['POST'])
def submit_client():
    '''Create a new client'''
    db = get_db()
    client = request.form['client_name'] # Grab client from form
    url = request.form['client_url'] if request.form['client_url'] else "https://{}.briostack.com".format(client)
    importUrl = request.form['client_import_url'] if request.form['client_import_url'] else "https://import.briostack.com/{}/webtools/control/main".format(client)
    db.execute('''INSERT INTO clients ([name], [import_url], [instance_url]) VALUES (?, ?, ?)''',
        [client, url, importUrl]
    )
    db.close()
    flash('Client submitted')
    return redirect(url_for('index'))


@MinimalMaps.route('/update_client_form')
def update_client_form():
    '''Form for submitting a new client'''
    check_login_status()
    db = get_db()
    statii = list(pd.read_sql("SELECT S.[status] FROM client_status AS S;", db).status)
    clients = list(pd.read_sql('''
        SELECT C.[name] 
        FROM clients AS C
        WHERE C.assignee='{}';'''.format(session['user']), db).name)
    db.close()
    return render_template('update_client_form.html', clients=clients, statii=statii)


@MinimalMaps.route('/update_client', methods=['POST'])
def update_client():
    '''Update an existing client'''
    check_login_status()

    db = get_db()
    form = request.form
    sql = "UPDATE clients SET [status] = '{0}' WHERE [name] = '{1}'".format(form['status'], form['client'])
    db.execute(sql)
    db.close()
    flash(sql)
    return redirect(url_for('index'))


# NOT WORKING
@MinimalMaps.route('/register', methods=['POST', 'GET'])
def register():
    '''Register a new user. NOT WORKING'''
    if not session.get('logged_in'):
        flash("Enter your credentials to crete an account")
        return render_template('register.html')
    else:
        return redirect(url_for('index'))


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


@MinimalMaps.route('/game')
def game():
    '''Play a little game'''
    check_login_status()
    return render_template('game.html')


@MinimalMaps.route('/login')
def login():
    '''User login page'''
    return render_template('login.html')

@MinimalMaps.route('/login_user', methods=['POST'])
def login_user():
    '''Log the user in'''
    error = None
    username, password = None, None
    combo = None
    db = get_db()
    data = db.execute('''SELECT username, [password] FROM users''') 

    combo = data.fetchone()
    while combo:
        username, password = combo
        checkname = request.form['username']
        checkpass = request.form['password']
        if checkname == username:
            if checkpass == password:
                session['logged_in'] = True
                session['user'] = checkname
                flash('Logged in')
                db.close()
                return redirect(url_for('index'))
            else:
                flash('Incorrect password')
        combo = data.fetchone()
    db.close()
    flash('Invalid username')
    
    return redirect(url_for('login'))

@MinimalMaps.route('/logout')
def logout():
    '''Log user out'''
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))