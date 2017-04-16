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
today = datetime.datetime.now()


################ Utils ################
def check_login_status(redirect_url='login'):
    '''Check to see if a user is logged in'''
    if not session.get('logged_in'):
        
        flash('You must be logged in to view this page')
        return redirect(url_for(redirect_url))


def setupPage():
    '''Check login and setup database'''
    check_login_status()
    db = get_db()
    return db


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




################ Homepage ################
@MinimalMaps.route('/')
def index():
    
    return render_template('index.html')




################ SQL Manipulation ################
@MinimalMaps.route('/submit_sql')
def submit_sql():
    '''Submit SQL for execution on the database'''
    check_login_status()
    return render_template('submit_sql.html')


@MinimalMaps.route('/execute', methods=['POST'])
def execute_sql():
    '''Execute the SQL statements'''
    db = setupPage()
    statements = request.form['sql'].split(';') # List of statements to execute

    for s in statements:
        s += ";" # Add an extra semicolon just in case...
        try:
            db.execute(s)
            flash(s)
        except:
            flash("{}".format(sys.exc_info()))
    db.close()
    return redirect(url_for('submit_sql'))




################ User Views ################
def get_colors(db):
    '''Get colors for data tables'''
    status_colors = pd.read_sql("SELECT [status], [color] FROM client_status", db).set_index('status').to_dict()['color']
    text_colors = pd.read_sql("SELECT [status], [text_color] FROM client_status", db).set_index('status').to_dict()['text_color']
    return status_colors, text_colors


@MinimalMaps.route('/my-clients')
def my_clients():
    '''View users clients. Only available to logged-in users'''
    db = setupPage()
    status_colors, text_colors = get_colors(db)
    
    client_data = pd.read_sql('''
    SELECT 
        [name], [status], [instance_url], [import_url], [estimated_completion], [import_notes], 
        [created_timestamp], [updated_timestamp]
    FROM 
        clients 
    WHERE 
        [assignee]='{}' '''.format(session['user']), db
    )

    db.close()
    return render_template('my_clients.html', data=client_data, 
    status_colors=status_colors, text_colors=text_colors)


@MinimalMaps.route('/client_statuses')
def client_statuses():
    '''Dashboard for viewing the status of all clients'''
    db = get_db()
    status_colors, text_colors = get_colors(db)
    client_data = pd.read_sql('''
        SELECT 
            [name], [status], [instance_url], [import_url], [assignee], 
            [estimated_completion], [import_notes], [created_timestamp], [updated_timestamp]
        FROM 
            clients''', db
    )
    
    # Convert to datetime columns
    client_data['created_timestamp'] = pd.to_datetime(client_data['created_timestamp'])
    client_data['updated_timestamp'] = pd.to_datetime(client_data['updated_timestamp'])

    # Days in queue and days since last update
    client_data['queue_days'] = [(today - _).days if not pd.isnull(today - _) else "" 
        for _ in client_data['created_timestamp']]
    
    client_data['update_days'] = [(today - _).days if not pd.isnull(today - _) else "" 
        for _ in client_data['updated_timestamp']]

    live_count = len(client_data[client_data.status == "Live"])
    
    db.close()

    return render_template('client_statuses.html', data=client_data, 
        status_colors=status_colors, text_colors=text_colors, live_count=live_count)




################ Submit clients ################
@MinimalMaps.route('/new_client_form', methods=['GET'])
def submit_client_form():
    '''Form for submitting a new client'''
    check_login_status()
    return render_template('submit_new_client.html')


def clean_client_name(string):
    '''Clean up the client name'''
    new_string = ""
    invalid_chars = "!@$%^&*)(}{][`~\'\"\\/><,.?;+=' "
    for s in string:
        if s not in invalid_chars:
            new_string += s
    return new_string if len(new_string) > 0 else None


@MinimalMaps.route('/submit_client', methods=['POST'])
def submit_client():
    '''Create a new client'''
    db = setupPage() # Establish credintials and connection
    client = request.form['client_name'] # Grab client from form
    client = clean_client_name(client)

    if client:
        instanceUrl = request.form['client_url'] if request.form['client_url'] else "https://{}.briostack.com".format(client)
        importUrl = request.form['client_import_url'] if request.form['client_import_url'] else "https://import.briostack.com/{}/webtools/control/main".format(client)
        timestamp = datetime.datetime.now().strftime('%D %T')

        try:
            
            db.execute('''
            INSERT INTO clients 
                ([name], [import_url], [instance_url], [created_timestamp], [updated_timestamp], [assignee]) 
            VALUES (?, ?, ?, ?, ?, ?);''',
                [client, instanceUrl, importUrl, timestamp, timestamp, session['user']]
            )

        except:
            
            flash('''Failed to submit "{}"'''.format(client))
            flash("{}".format(sys.exc_info()))
            
            db.close()
            return redirect(url_for('submit_client_form'))
        
        flash('Client submitted')
        db.close()
        return redirect(url_for('my_clients'))
    else:
        flash('Client name required')
        db.close()
        return redirect(url_for('submit_client_form'))




################ Update client database ################
@MinimalMaps.route('/update_client_form')
def update_client_form():
    '''Form for submitting a new client'''
    db = setupPage()
    
    statii = pd.read_sql('''
    SELECT S.[status] 
    FROM client_status AS S;''', db)

    clients = pd.read_sql('''
        SELECT C.[name] 
        FROM clients AS C
        WHERE C.assignee='{}';'''.format(session['user']), db)
    
    clients = list(clients.name) # List of clients associated with user
    statii = list(statii.status) # List of statuses to updates to
    
    db.close()

    return render_template('update_client_form.html', clients=clients, statii=statii)

def execute_updates(db, execution_string):
    try:
        db.execute(execution_string)
        flash(execution_string)
    except:
        # Flash messages
        flash('''Failed to update "{}"'''.format(client))
        flash("{}".format(sys.exc_info()))


def fix_input_string(string):
    new_string = ""
    invalid_chars = ""
    for s in string:
            if s not in invalid_chars:
                if s in "\'\"":
                    new_string += "\\"
                new_string += s
    return new_string


@MinimalMaps.route('/update_client', methods=['POST'])
def update_client():
    '''Update an existing client'''

    
    # Form extraction
    client = request.form['client']
    status = request.form['status']
    import_notes = fix_input_string(request.form['import_notes']) # This may be vulnerable.
    est_completion = fix_input_string(request.form['estimated_completion'])
    timestamp = datetime.datetime.now().strftime('%D %T')

    db = setupPage() # Connect to database
        
    if client:
        update_status = '''UPDATE clients SET 
            [status] = '{}', [updated_timestamp] = '{}' WHERE [name] = '{}';'''.format(status, timestamp, client)
        execute_updates(db, update_status)
    
        if est_completion:
            update_est_completion = '''UPDATE clients SET [est_completion] = '{}' WHERE [name] = '{}';'''.format(est_completion, client)
            execute_updates(db, update_est_completion)
        
        if import_notes:
            update_import_notes = '''UPDATE clients SET [import_notes] = '{}' WHERE [name] = '{}';'''.format(import_notes, client)
            execute_updates(db, update_import_notes)

    db.close()

    return redirect(url_for('my_clients'))




################ User registration (not working as of 4/15/2017) ################
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




################ User login ################
@MinimalMaps.route('/login')
def login():
    '''User login page'''
    return render_template('login.html')


@MinimalMaps.route('/login_user', methods=['POST'])
def login_user():
    '''Log the user in'''
    username, password = None, None
    combo = None

    db = get_db()

    data = db.execute('''SELECT username, [password] FROM users''') # Grab users

    combo = data.fetchone() # Grab first username/password combo
    while combo: # Iterate while there's still data
        username, password = combo # Set username and password

        # Grab form details
        checkname = request.form['username']
        checkpass = request.form['password']

        # Comparison checks
        if checkname == username:
            if checkpass == password:
                # Login successful
                session['logged_in'] = True
                session['user'] = checkname
                flash('Welcome {}'.format(checkname))
                db.close() # Close db connection
                return redirect(url_for('my_clients')) # Redirect to my clients
            else:
                flash('Incorrect password')
        combo = data.fetchone() # grab the next one
    flash('Invalid username') # Couldn't find user name
    db.close() # Close db connection
    return redirect(url_for('login'))


@MinimalMaps.route('/logout')
def logout():
    '''Log user out'''
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))



################ A little game I made ################
@MinimalMaps.route('/game')
def game():
    '''Play a little game'''
    check_login_status()
    return render_template('game.html')
