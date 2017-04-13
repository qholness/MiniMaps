import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

MinimalMaps = Flask(__name__) # Create MinimalMapslication instance
MinimalMaps.config.from_object(__name__)
dbPath = 'sqlite:///MiniMaps/MiniMaps/data/database.db'
MinimalMaps.config.update(dict(
    DATABASE=os.path.join(dbPath),
    SECRET_KEY='tempDevConfig',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=dbPath
    )
)

database = SQLAlchemy(MinimalMaps)
migrate = Migrate(MinimalMaps, database)