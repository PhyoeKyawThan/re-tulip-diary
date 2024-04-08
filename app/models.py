from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable= False)
    email = db.Column(db.String(100), nullable=False)
    registered_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(255), nullable=False)
    posts   = db.relationship("Post", backref="author", lazy=True)
    
class Post(db.Model):
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caption = db.Column(db.String(255), default="")
    image_uri = db.Column(db.String(255), default="")
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    comments = db.relationship("Comment", backref="aurthor", lazy=True)

class Comment(db.Model):
    ___tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(200), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)