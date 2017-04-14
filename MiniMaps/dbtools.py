from MiniMaps import MinimalMaps
from MiniMaps import database
from sqlite3 import dbapi2 as sqlite3
from flask import g
import sqlalchemy as sql




def init_db():
    """Initializes the database."""
    db = get_db()
    with MinimalMaps.open_resource('/MiniMaps/MiniMaps/data/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def connect_db():
    engine = sql.create_engine(MinimalMaps.config['SQLALCHEMY_DATABASE_URI'])
    connection = engine.connect()
    connection.row_factory = sqlite3.Row
    return connection

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@MinimalMaps.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@MinimalMaps.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
