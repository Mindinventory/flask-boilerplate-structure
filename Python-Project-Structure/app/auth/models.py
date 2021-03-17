from app import db


# Define a Base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Define User model which inherit Base model
class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    confirmation = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(192), nullable=False)

    # New instance instantiation procedure
    def __init__(self, public_id, first_name, last_name, email, password):
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


    def __repr__(self):
        return '<User %r>' % self.email
