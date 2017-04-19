import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sslify import SSLify

MinimalMaps = Flask(__name__) # Create MinimalMapslication instance
MinimalMaps.config.from_object(__name__)


engine_string = 'sqlite:///MiniMaps/data/database.db'
dbPath = '/MiniMaps/data/database.db'


MinimalMaps.config.update(dict(
    DATABASE=os.path.join(MinimalMaps.root_path, dbPath),
    SECRET_KEY='tempDevConfig',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=engine_string
    )
)

sslify = SSLify(MinimalMaps, subdomains=True, permanent=True)
database = SQLAlchemy(MinimalMaps)
migrate = Migrate(MinimalMaps, database)