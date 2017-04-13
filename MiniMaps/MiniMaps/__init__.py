from flask import Flask
import flask_migrate
import flask_sqlalchemy

MinimalMaps = Flask(__name__) # Create MinimalMapslication instance
MinimalMaps.config.from_object(__name__)
MinimalMaps.config.update(dict(
    DATABASE=os.path.join(MinimalMaps.root_path + '/data/database.db'),
    SECRET_KEY='tempDevConfig',
    )
)