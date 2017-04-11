from __init__ import MinimalMaps
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from dbtools import *
import pandas as pd

@MinimalMaps.route('/')
def index():
    db = get_db()
    cur = db.execute('''SELECT * FROM stations''')
    stations = cur.fetchall()
    return render_template('index.html', 
    stations=stations
    )


@MinimalMaps.route('/testpost')
def test():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    data = pd.read_sql('''SELECT * FROM cta_buses''', db)[:1000]

    # Normalize lat and lon
    data['POINT_X'] = data['POINT_X'].astype(float)
    data['POINT_Y'] = data['POINT_Y'].astype(float)

    meanx = data.POINT_X.mean()
    meany = data.POINT_Y.mean()
    sdevx = data.POINT_X.std()
    sdevy = data.POINT_Y.std()

    normalize = lambda value, mean, sdev: (value - mean)/sdev

    data['POINT_X'] = [normalize(_, meanx, sdevx) for _ in data['POINT_X']]
    data['POINT_Y'] = [normalize(_, meany, sdevy) for _ in data['POINT_Y']]

    xmulpt = 720 / max(data.POINT_X)
    ymulpt = 480 / max(data.POINT_Y)

    data['POINT_X'] = [abs(_) * xmulpt for _ in data['POINT_X']]
    data['POINT_Y'] = [abs(_) * ymulpt for _ in data['POINT_Y']]

    flash('Added data!')
    return render_template('test.html', data=data)


@MinimalMaps.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    db = get_db()
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
            return redirect(url_for('test'))

    return render_template('login.html', error=error)


@MinimalMaps.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))