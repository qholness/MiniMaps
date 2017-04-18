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
import random
global today
today = lambda: datetime.datetime.now()


################ Utils ################
def check_login_status():
    '''Check to see if a user is logged in'''
    if not session.get('logged_in', None):
        
        flash('Info: You must be logged in to view this page')

        return 1


@MinimalMaps.route('/change-password')
def change_password():
    '''Change a password'''
    if check_login_status():
        return redirect(url_for('login'))
    
    return render_template('change_password.html')


@MinimalMaps.route('/execute-change-password', methods=['POST'])
def execute_change_password():
    '''Change a user password'''
    if check_login_status():
        return redirect(url_for('login'))
    
    # Get form data
    old_password = request.form['oldPassword']
    new_password = request.form['newPassword']
    conf_password = request.form['newPassConf']

    # Password field is blank
    if not new_password:
        flash("Fail: Password field cannot be blank")
        return redirect(url_for('change_password'))
    
    # Password too short
    if len(new_password) < 5:
        flash("Warning: Password is too short ")
        return redirect(url_for('change_password'))
    
    # Password too long
    if len(new_password) > 64:
        flash("Warning: Password is too long")
        return redirect(url_for('change_password'))
    
    # Special characters
    special_chars = '''}*'"{][]},./<>?\\|`~%^='''
    for s in new_password:
        if s in special_chars:
            flash("Warning: {} is not allowed.".format(s))
            return redirect(url_for('change_password'))

    # Connect to database
    db = get_db()
    getpass = "SELECT [password] FROM users WHERE [username] = '{}'".format(session['user'])
    checkPass = list(pd.read_sql(getpass, db).password)[0]

    # Make sure old password is correct
    if old_password != checkPass:
        flash("Fail: Old password was incorrect")
        return redirect(url_for('change_password'))
    
    # Check to see if passwords match
    if new_password != conf_password:
        flash("Warning: Passwords don't match")
        return redirect(url_for('change_password'))
    
    try:
    
        db.execute('''UPDATE users
            SET [password] = ?
            WHERE [username] = ?
            ''', (new_password, session['user'])
        )
        flash("Success: Password change was successful")
        db.close()
        return redirect(url_for('my_clients'))
    
    except:

        flash("Failed to change password")
        flash("Fail: {}".format(sys.exc_info()))
        db.close()
        return redirect(url_for('change_password'))


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
@MinimalMaps.route('/sql_out')
def submit_sql():
    '''Submit SQL for execution on the database'''
    check_login_status()
    data = None
    if session.get('data'):
        data = {key : pd.read_json(value) for key, value in session['data'].items()}
        session.pop('data')
    else:
        return redirect(url_for(my_clients))
    return render_template('submit_sql.html', data=data)


@MinimalMaps.route('/execute', methods=['POST'])
def execute_sql():
    '''Execute the SQL statements'''
    # Check if user is logged-in
    if check_login_status():
        return redirect('login')
    
    db = get_db() # Get db connection

    statements = request.form['sql'].split(';') # List of statements to execute (splitting on ";")
    
    session['data'] = {} # Init session data hash
    
    for s in statements:
        s += ";" # Add an extra semicolon just in case...
        try:
            if "select" in s.lower(): # If a select statement, push select output to session['data']
                session['data'][s] = pd.read_sql(s, db).to_json() # Hash results to select statement
            else:
                db.execute(s)
                flash("Success".format(s))
        except:
            flash("Fail: {}".format(sys.exc_info()))
    
    db.close()
    
    return redirect(url_for('submit_sql'))




################ User Views ################
def get_colors(db):
    '''Get colors for data tables'''
    status_colors = pd.read_sql("SELECT [status], [color] FROM client_status", db).set_index('status').to_dict()
    text_colors = pd.read_sql("SELECT [status], [text_color] FROM client_status", db).set_index('status').to_dict()
    return status_colors, text_colors


@MinimalMaps.route('/my-clients')
def my_clients():
    '''View users clients. Only available to logged-in users'''
    if check_login_status():
        return redirect('login')
        
    db = get_db()

    status_colors, text_colors = get_colors(db)
    text_colors = text_colors['text_color']
    status_colors = status_colors['color']
    statii = list(status_colors.keys())
    clients = list(pd.read_sql('''SELECT DISTINCT [name] FROM clients;''', db)['name'])
    users = list(pd.read_sql('''SELECT DISTINCT [username] FROM users;''', db)['username'])
    client_data = pd.read_sql('''
    SELECT 
        [name], [status], [instance_url], [import_url], [estimated_completion], [import_notes], 
        [created_timestamp], [updated_timestamp]
    FROM 
        clients 
    WHERE 
        [assignee]='{}' '''.format(session['user']), db
    )
    
    myClients = list(client_data['name'])

    db.close()
    return render_template('my_clients.html', data=client_data, 
    status_colors=status_colors, text_colors=text_colors, statii=statii, clients=clients, users=users, myClients=myClients)


@MinimalMaps.route('/client_statuses')
def client_statuses():
    '''Dashboard for viewing the status of all clients'''
    db = get_db() # Connect to database
    status_colors, text_colors = get_colors(db)
    status_colors = status_colors['color']
    text_colors = text_colors['text_color']
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
    day_dif = lambda x: today() - x
    client_data['queue_days'] = [day_dif(_).days if not pd.isnull(day_dif(_)) else "" 
        for _ in client_data['created_timestamp']] # Days since created
    
    client_data['update_days'] = [day_dif(_).days if not pd.isnull(day_dif(_)) else "" 
        for _ in client_data['updated_timestamp']] # Days since last updated
    
    counts = client_data.status.value_counts() # Counts of status types {type : count}
    
    db.close()

    titles = ['Dat Dashboard Tho', 'Briostack Client On-Boarding', 'Data Migration Dashboard',
    'Data Junkies', 'Client Statuses']
    title = titles.pop(random.randint(0, len(titles) - 1))

    return render_template('client_statuses.html', data=client_data, 
        status_colors=status_colors, text_colors=text_colors, title=title, counts=counts)




################ Submit clients ################

## Considering depricating
# @MinimalMaps.route('/new_client_form', methods=['GET'])
# def submit_client_form():
#     '''Form for submitting a new client'''
#     check_login_status()
#     return render_template('submit_new_client.html')


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
    if check_login_status(): # Establish credintials and connection
        return redirect('login')
    db = get_db()

    client = request.form['client_name'] # Grab client from form
    client = clean_client_name(client)

    if client:
        instanceUrl = request.form['client_url'] if request.form['client_url'] else "https://{}.briostack.com".format(client)
        importUrl = request.form['client_import_url'] if request.form['client_import_url'] else "https://import.briostack.com/{}/webtools/control/main".format(client)
        timestamp = datetime.datetime.now().strftime('%D %T')

        try:
            
            db.execute('''
            INSERT INTO clients 
                ([name], [status], [instance_url], [import_url], [created_timestamp], [updated_timestamp], [assignee]) 
            VALUES (?, ?, ?, ?, ?, ?, ?);''',
                [client, "Open", instanceUrl, importUrl, timestamp, timestamp, session['user']]
            )
            flash("Success importing")
            
        except:
            
            flash('''Failed to submit "{}"'''.format(client))
            flash("Failed: {}".format(sys.exc_info()))
            
            db.close()
            return redirect(url_for('submit_client_form'))
        
        flash('Success: {} submitted'.format(client))
        db.close()
        return redirect(url_for('my_clients'))
    else:
        flash('Fail: Client name required')
        db.close()
        return redirect(url_for('submit_client_form'))




################ Update client database ################

## Considering depricating
# @MinimalMaps.route('/update_client_form')
# def update_client_form():
#     '''Form for submitting a new client'''
#     if check_login_status():
#         return redirect('login')
#     db = get_db()

    
#     statii = pd.read_sql('''
#     SELECT S.[id], S.[status] 
#     FROM client_status AS S;''', db).sort_values('id', ascending=True)

#     clients = pd.read_sql('''
#         SELECT C.[name] 
#         FROM clients AS C
#         WHERE C.assignee='{}';'''.format(session['user']), db).sort_values('name', ascending=True)
    
#     clients = list(clients.name) # List of clients associated with user
#     statii = list(statii.status) # List of statuses to updates to
    
#     db.close()

#     return render_template('update_client_form.html', clients=clients, statii=statii)

def execute_updates(db, execution_string):
    try:
        db.execute(execution_string)
        flash("Success: {}".format(execution_string))
    except:
        # Flash messages
        flash('''Fail to update "{}"'''.format(client))
        flash("Fail: {}".format(sys.exc_info()))


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

    if check_login_status(): # Connect to database:
        return redirect('login')
    
    
    db = get_db()

        
    if client:
        # Update client
        if status:
            db.execute('''UPDATE clients 
                SET [status] = ?, [updated_timestamp] = ?
                WHERE [name] = ?;''', (status, timestamp, client)
            )
        
        if est_completion:
            # Update est_completion if requested
            db.execute('''UPDATE clients 
                SET [est_completion] = ? 
                WHERE [name] = ?;''', (est_completion, client)
            )
        
        if import_notes:
            # Only update notes if passed
            db.execute('''UPDATE clients 
                SET [import_notes] = ? 
                WHERE [name] = ?;''', (import_notes, client)
            )
    else:
    
        flash("No client selected")
    
    db.close()

    return redirect(url_for('my_clients'))


@MinimalMaps.route('/view-note')
def full_note():
    return request.args.get('note')



################ User registration (not working as of 4/15/2017) ################
@MinimalMaps.route('/register', methods=['POST', 'GET'])
def register():
    '''Register a new user. NOT WORKING'''
    if not session.get('logged_in'):
        flash("Info: Enter your credentials to crete an account")
        return render_template('register.html')
    else:
        return redirect(url_for('index'))


@MinimalMaps.route('/exchange_client')
def exchange_clients():
    '''Allow users to pick up or remove extra clients'''
    if check_login_status():
        return redirect('login')
    db = get_db()

    clients = list(pd.read_sql('''SELECT DISTINCT [name] from clients''', db)['name'])
    users = list(pd.read_sql('''SELECT DISTINCT username from users''', db)['username'])
    
    return render_template('exchange_clients.html', clients=clients, users=users)


@MinimalMaps.route('/execute-client-exchange', methods=['POST'])
def execute_exchange():
    '''Execute client exchange'''
    if check_login_status():
        return redirect('login')
    
    db = get_db()

    try:
        giveTo = request.form['giveTo']
        client = request.form['client']
        db.execute('''UPDATE clients
        SET [assignee] = ?
        WHERE [name] = ?
        ''', (giveTo, client)
        )
        flash("Success: Updated assignee of \"{}\" to {}".format(client, giveTo))
    except:
        flash("Fail: {}".format(sys.exc_info()))
    db.close()
    return redirect(url_for('client_statuses'))

    

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
    return render_template('login.html', _scheme="https")


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
                session['login_time'] = today()
                flash('Success: Welcome {}'.format(checkname))
                db.close() # Close db connection
                return redirect(url_for('my_clients')) # Redirect to my clients
            else:
                flash('Fail: Incorrect password')
        combo = data.fetchone() # grab the next one
    flash('Fail: Invalid username') # Couldn't find user name
    db.close() # Close db connection
    return redirect(url_for('login'))


@MinimalMaps.route('/logout')
def logout():
    '''Log user out'''
    session.pop('user', None)
    session.pop('logged_in', None)
    session.pop('login_time', None)
    flash('Success: You were logged out')
    return redirect(url_for('login'))



################ A little game I made ################
@MinimalMaps.route('/game')
def game():
    '''Play a little game'''
    check_login_status()
    return render_template('game.html')
