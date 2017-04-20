from MiniMaps import MinimalMaps
from MiniMaps.dbtools import *
from MiniMaps.models import *
from MiniMaps.utils import *
from flask import request, session, redirect, url_for, abort, render_template, flash
import pandas as pd
import datetime
import hashlib
import base64
import uuid
import sys


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
    
    if not session.get('user_data'):
        session['user_data'] = row_zero(
            pd.read_sql('''
                SELECT * 
                FROM users 
                WHERE [username] = '{}';'''
                .format(session['user']), db)
            .to_dict('list')
        ) # Data for user's data table
    
    db.close()

    return render_template('me.html', user_data=session.get('user_data'))

################ User views ################
@MinimalMaps.route('/game')
def game():
    
    return render_template('game.html')