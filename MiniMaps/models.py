from MiniMaps import database as db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True, nullable=False)
    image_url = db.Column(db.String(), unique=False, nullable=True)
    rights = db.Column(db.String(), unique=False, nullable=True)

    def __init__(self, username, email, password, image_url):
        self.username = username
        self.email = email
        self.password = password
        self.image_url = image_url
        self.rights = 'Normal'

    def __repr__(self):
        return '<User %r' % self.username




class Venues(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(80), unique=True, nullable=False)
    venueAddress = db.Column(db.String(), unique=False)
    venueCity = db.Column(db.String(), unique=False)
    venueState = db.Column(db.String(), unique=False)
    venue_email = db.Column(db.String(120), unique=True, nullable=True)
    latitude = db.Column(db.String(), unique=False, nullable=True)
    longitude = db.Column(db.String(), unique=False, nullable=True)

    def __init__(self, venue_name, venue_email, venueAddress, 
    venueCity, venueState, latitude, longitude):
        self.venue_name = venue_name
        self.venue_email = venue_email
        self.venueAddress = venueAddress
        self.venueCity = venueCity
        self.venueState = venueState
        self.latitude = latitude
        self.longitude = longitude
        self.image_url = image_url

    def __repr__(self):
        return '<User %r' % self.username



# class Sequence(db.Model):
#     __tablename__ = 'sqlite_sequence'
#     name = db.Column(db.String())
#     seq = db.Column(db.String())