from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    hotels = db.relationship('Hotels')  # This creates a one to many relationships to the Hotels table

class Hotels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    services = db.Column(db.String(250))
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))