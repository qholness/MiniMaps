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
global timestamp, max_submission_count
max_submission_count = 5
timestamp = lambda : datetime.datetime.strftime(datetime.datetime.utcnow(), "%D %T")


def init_match_table():
     return pd.DataFrame(
            {
                'p1' : [],
                'p2' : [], 
                'char1' : [], 
                'char2' : [],
                'winner' : [],
                'league' : [], 
                'game' : [],
                'timestamp' : []
            },
            index=[]
        ).to_json()

@MinimalMaps.route('/ranbat')
def event():
    if not session.get('user'):
        flash('You must be logged in to view this page', 'warning')
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


@MinimalMaps.route('/ranbat-create-league', methods=['GET', 'POST'])
def get_league_data():
    '''?'''
    session['user_status'] = "TO"
    if not session.get('user_status'):
        flash("You must create a tournament to view this page", 'info')
        return redirect(url_for('event'))
    league = request.form.get('league', None)
    game = request.form.get('game', None)

    if not league:
        league = session.get('league')
        if not league:
            flash("No league selected")
            return redirect(url_for('event'))
    
    if not game:
        game = session.get('game')
        if not game:
            flash('No game selected')
            return redirect(url_for('event'))
    
    session['league'] = league
    session['game'] = game
    session['row_count'] = 0

    if not session.get('matchTable'):
        # Must be JSON?
        session['matchTable'] = init_match_table()

    db = get_db()

    characters = get_characters(db, game)
    players = get_players(db, league)
    
    db.close()

    return render_template('generate_ranbat.html', players=players, characters=characters, 
    league=league, game=game, data=pd.read_json(session.get('matchTable')))


@MinimalMaps.route('/submit-match', methods=['POST'])
def submitMatch():
    '''Post method for submitting a match to the database'''
    db = get_db()
    
    p1 = request.form.get('p1')
    p2 = request.form.get('p2')
    
    char1 = request.form.get('char1')
    char2 = request.form.get('char2')
    winner = request.form.get('winner')
    
    game = session.get('game')
    league = session.get('league')
    

    characters = get_characters(db, game)
    players = get_players(db, league)

    if p1 == p2:
        flash("Same player selected. Please try again", 'danger')
        return redirect(url_for('get_league_data'))

    if not p1:
        flash("Player 1 was not selected", 'danger')
        return redirect(url_for('get_league_data'))
    
    if not p2:
        flash("Player 1 was not selected", 'danger')
        return redirect(url_for('get_league_data'))

    if not char1:
        flash("Player 1's character was not selected", 'danger')
        return redirect(url_for('get_league_data'))
    
    if not char2:
        flash("Player 2's character was not selected", 'danger')
        return redirect(url_for('get_league_data'))

    if not winner:
        flash("Winner was not selected", 'danger')
        return redirect(url_for('get_league_data'))
    
    db = get_db()

    session['row_count'] +=  1
    try:
        # Add match to session table
        
        temp = pd.read_json(session['matchTable'])

        while True:
            try:
                session['matchTable'] = temp.append(
                    pd.DataFrame(
                        {
                            'p1' : [p1],
                            'p2' : [p2], 
                            'char1' : [char1], 
                            'char2' : [char2],
                            'winner' : [winner],
                            'league' : [league], 
                            'game' : [game],
                            'timestamp' : [timestamp()]
                        },
                        index=[session['row_count']]
                    )
                ).to_json()
                
                break
            
            except ValueError:
            
                session['row_count'] +=  1

        if len(pd.read_json(session['matchTable'])) > max_submission_count:
            flash("Submitting data to database", 'info')
            return redirect(url_for('end_ranbat_continue'))
        
        flash("Submitted match. Create another or end ranbat", 'success')
        
        db.close()

        return redirect(url_for('get_league_data'))
    
    except:
        
        flash('Failed to submit match', 'danger')

        db.close()

        print("{}".format(sys.exc_info()))

        return redirect(url_for('get_league_data'))



@MinimalMaps.route('/end-ranbat')
def end_ranbat():
    '''End ranbat for a user'''
    # Push to database
    db = get_db()
    tempTable = pd.read_json(session['matchTable'])
    if len(tempTable) == 0: return redirect(url_for('showMe'))
    failed_rows = 0
    scucceeded_rows = 0
    faildf = []

    for index, row in tempTable.iterrows():
        try:
            submission = (row['p1'], row['p2'], row['char1'], row['char2'],
                    row['winner'], row['game'], row['league'], str(row['timestamp']))
            
            db.execute('''
                INSERT INTO matchLog ([p1],[p2],[char1],[char2], 
                    [winner],[game],[league],[timestamp])
                VALUES (?,?,?,?,?,?,?,?)''',
                (submission)
            )
            scucceeded_rows += 1

        except:
            print("{}".format(sys.exc_info()))
            failed_rows += 1
            if len(faildf) == 0:
                faildf = pd.DataFrame(
                    {
                        'p1' : row['p1'],
                        'p2' : row['p2'],
                        'char1' : row['char1'],
                        'char2' : row['char2'],
                        'winner' : row['winner'],
                        'game' : row['game'],
                        'league' : row['league'],
                        'timestamp' : row['timestamp']
                    },
                    index=[failed_rows]
                )
            else:
                faildf = faildf.append(
                    pd.DataFrame(
                        {
                            'p1' : row['p1'],
                            'p2' : row['p2'],
                            'char1' : row['char1'],
                            'char2' : row['char2'],
                            'winner' : row['winner'],
                            'game' : row['game'],
                            'league' : row['league'],
                            'timestamp' : row['timestamp']
                        },
                    index=[failed_rows]
                    )
                )

    db.close()
    
    if len(faildf) > 0: session['failed_matches'] = faildf.to_json()

    session.pop('matchTable')
    session.pop('league')
    session.pop('game')

    flash('Pushed {} out of {} matches'.format(scucceeded_rows, scucceeded_rows + failed_rows),'info')
    
    return redirect(url_for("showMe"))


@MinimalMaps.route('/end-ranbat-continue')
def end_ranbat_continue():
    '''End ranbat for a user'''
    # Push to database
    db = get_db()
    tempTable = pd.read_json(session['matchTable'])
    failed_rows = 0
    scucceeded_rows = 0
    faildf = []

    for index, row in tempTable.iterrows():
        try:
            submission = (row['p1'], row['p2'], row['char1'], row['char2'],
                    row['winner'], row['game'], row['league'], str(row['timestamp']))
            
            db.execute('''
                INSERT INTO matchLog ([p1],[p2],[char1],[char2], 
                    [winner],[game],[league],[timestamp])
                VALUES (?,?,?,?,?,?,?,?)''',
                (submission)
            )
            scucceeded_rows += 1

        except:
            print("{}".format(sys.exc_info()))
            failed_rows += 1
            if len(faildf) == 0:
                faildf = pd.DataFrame(
                    {
                        'p1' : row['p1'],
                        'p2' : row['p2'],
                        'char1' : row['char1'],
                        'char2' : row['char2'],
                        'winner' : row['winner'],
                        'game' : row['game'],
                        'league' : row['league'],
                        'timestamp' : row['timestamp']
                    },
                    index=[failed_rows]
                )
            else:
                faildf = faildf.append(
                    pd.DataFrame(
                        {
                            'p1' : row['p1'],
                            'p2' : row['p2'],
                            'char1' : row['char1'],
                            'char2' : row['char2'],
                            'winner' : row['winner'],
                            'game' : row['game'],
                            'league' : row['league'],
                            'timestamp' : row['timestamp']
                        },
                    index=[failed_rows]
                    )
                )

    db.close()
    
    if len(faildf) > 0: session['failed_matches'] = faildf.to_json()

    session.pop('matchTable')

    flash('Pushed {} out of {} matches'.format(scucceeded_rows, scucceeded_rows + failed_rows), 'success' if scucceeded_rows > failed_rows else 'danger')
    
    return redirect(url_for("get_league_data"))