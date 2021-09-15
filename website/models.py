from . import db  # importing the db variable from __init__ file
from flask_login import UserMixin
from sqlalchemy.sql import func  # for current time

# Creating a database model by inheriting from db.model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
