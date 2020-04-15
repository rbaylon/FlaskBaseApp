from baseapp import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

class Lte(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.Integer)
    archive = db.Column(db.Integer)
    error = db.Column(db.Integer)
    drop = db.Column(db.Integer)
    rdate = db.Column(db.String(10))
    location = db.Column(db.String(10))


