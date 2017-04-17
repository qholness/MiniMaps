from MiniMaps import database as db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String())
    rights = db.Column(db.String())
    league = db.Column(db.String())
    region = db.Column(db.String())

    def __init__(self, username, email, password, image_url):
        self.username = username
        self.email = email
        self.password = password
        self.image_url = image_url
        self.rights = 'Normal'

    def __repr__(self):
        return '<User %r' % self.username


class UserData(db.Model):
    __tablename__ = 'userData'
    username = db.Column(db.String(80), primary_key=True)
    games = db.Column(db.String(80))
    characters = db.Column(db.String(80))

class Leagues(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    image_url = db.Column(db.String())
    facebookUrl = db.Column(db.String())
    region = db.Column(db.String())


class Regions(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    image_url = db.Column(db.String())


class Venues(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(80), unique=True, nullable=False)
    venueAddress = db.Column(db.String(), unique=False)
    venueCity = db.Column(db.String(), unique=False)
    venueState = db.Column(db.String(), unique=False)
    venue_email = db.Column(db.String(120))
    region = db.Column(db.String())
    latitude = db.Column(db.String())
    longitude = db.Column(db.String())

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


class game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    
    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String())
    game = db.Column(db.String())

class MatchLog(db.Model):
    __tablename__ = 'matchLog'
    id = db.Column(db.Integer, primary_key=True)
    p1 = db.Column(db.String())
    p2 = db.Column(db.String())
    char1 = db.Column(db.String())
    char2 = db.Column(db.String())


# class Sequence(db.Model):
#     __tablename__ = 'sqlite_sequence'
#     name = db.Column(db.String())
#     seq = db.Column(db.String())