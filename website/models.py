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
    posts = db.relationship("Post", backref="user", passive_deletes=True)
    comments = db.relationship("Comment", backref="user", passive_deletes=True)
    likes = db.relationship("Like", backref="user", passive_deletes=True)
    # backref='user' allows a post to access the entire user a post belongs to (ex. post.user.<property>)
    # passive_deletes=True deletes all associated post with a user


# lowercase user as an argument in foreignkey to reference the user in the database
# ondelete="CASCADE" allows the user to delete all the post via(passive_deletes) when the user is deleted
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)  # nullable cannot be empty
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    comments = db.relationship("Comment", backref="post", passive_deletes=True)
    likes = db.relationship("Like", backref="post", passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
