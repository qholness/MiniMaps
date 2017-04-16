from MiniMaps import database as db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String())
    rights = db.Column(db.String())

    def __init__(self, username, email, password, image_url):
        self.username = username
        self.email = email
        self.password = password
        self.image_url = image_url
        self.rights = 'Normal'

    def __repr__(self):
        return '<User %r' % self.username




class Status(db.Model):
    __tablename__ = 'client_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, unique=True, nullable=False)
    color = db.Column(db.String, unique=True)
    text_color = db.Column(db.String, unique=True)

    def __init__(self, status):
        statii = ('scripting', 'cleaning', 'importing', 'import_complete', 'on_hold','') # list of statuses
        self.status = status if status in statii else None



class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    import_url = db.Column(db.String(), unique=False)
    instance_url = db.Column(db.String(), unique=False)
    assignee = db.Column(db.String())
    status = db.Column(db.String())
    import_notes = db.Column(db.String())
    estimated_completion = db.Column(db.String())
    created_timestamp = db.Column(db.String())
    updated_timestamp = db.Column(db.String())
    
    def __init__(self, name, import_url, instance_url, assignee,status, estimated_completion):
        self.name = name
        self.import_url = import_url
        self.instance_url = instance_url
        self.assignee = assignee
        self.status = status
        self.import_notes = import_notes
        self.estimated_completion = estimated_completion

    def __repr__(self):
        return '<User %r' % self.username



# class Sequence(db.Model):
#     __tablename__ = 'sqlite_sequence'
#     name = db.Column(db.String())
#     seq = db.Column(db.String())