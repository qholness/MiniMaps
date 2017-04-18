from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from flask import request, session, redirect, url_for, abort, render_template, flash
import pandas as pd
import datetime
import hashlib
import base64
import uuid
import sys
global today
today = lambda : datetime.datetime.strftime(datetime.datetime.now(), "%D %T")



################ utils ####################
row_zero = lambda data: {k : v[0] for k, v in data.items()}




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
    flash('You are already logged in')
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


@MinimalMaps.route('/ranbat')
def event():
    if not session.get('user'):
        flash('You must be logged in to view this page')
        return redirect(url_for('index'))
    db = get_db()
    
    leagues = pd.read_sql('''
        SELECT DISTINCT [name] 
        FROM leagues 
        ;''', db).to_dict('list')['name']
    
    games = pd.read_sql('''
        SELECT DISTINCT [name]
        FROM game
        ;''', db).to_dict('list')['name']
    
    db.close()
   
    return render_template('ranbat.html', leagues=leagues, games=games)

def get_players(db, league):
    '''Get league players query'''
    players = pd.read_sql('''
        SELECT [username]
        FROM users
        WHERE [league]='{}'
        ;'''.format(league), db).to_dict('list')['username']

    return players
    
def get_characters(db, game):
    '''Get game characters query'''
    characters = pd.read_sql('''
        SELECT [character]
        FROM characters
        WHERE game='{}'
        ;'''.format(game), db).to_dict('list')['character']
    
    return characters


@MinimalMaps.route('/ranbat-create-league', methods=['POST', 'GET'])
def get_league_data():
    league = request.form.get('league', None)
    game = request.form.get('game', None)
    
    if not league:
        flash("No league selected")
        return redirect(url_for('event'))
    
    if not game:
        flash('No game selected')
        return redirect(url_for('event'))

    db = get_db()

    characters = get_characters(db, game)
    players = get_players(db, league)
    
    db.close()

    return render_template('generate_ranbat.html', players=players, characters=characters, 
    league=league, game=game)


@MinimalMaps.route('/submit-match', methods=['POST'])
def submitMatch():
    
    p1 = request.form.get('p1')
    p2 = request.form.get('p2')
    char1 = request.form.get('char1')
    char2 = request.form.get('char2')
    request.span.get('game')
    characters = get_characters(db, request.form.get('game'))
    players = get_players(db, request.form.get('league'))

    if p1 == p2:
        flash("Same player selected. Please try again")
        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)

    if not p1:
        flash("Player 1 was not selected")
        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)
    
    if not p2:
        flash("Player 1 was not selected")
        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)

    if not char1:
        flash("Player 1 was not selected")
        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)
    
    if not char2:
        flash("Player 1 was not selected")
        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)

    db = get_db()

    try:
        
        db.execute('''
            INSERT INTO matchLog ([p1], [p2],[char1],[char2])
            VALUES (?,?,?,?)''', [p1, p2, char1, char2]
        )
        
        flash("Submitted match. Create another of end ranbat")
        
        db.close()

        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)
    
    except:
        
        flash('Failed to submit match')

        db.close()

        print("{}".format(sys.exc_info()))

        return render_template('generate_ranbat.html', players=players, characters=Characters, league=league, game=game)