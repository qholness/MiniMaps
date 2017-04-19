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
global timestamp
timestamp = lambda : datetime.datetime.strftime(datetime.datetime.utcnow(), "%D %T")



################ utils ####################
row_zero = lambda data: {k : v[0] for k, v in data.items()}


@MinimalMaps.route('/')
def index():
    
    return render_template('index.html')

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