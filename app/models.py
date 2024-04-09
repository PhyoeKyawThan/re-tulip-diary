from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable= False)
    profile_uri = db.Column(db.String(150), nullable=True, default="/static/images/profile/anonymous.png")
    email = db.Column(db.String(100), nullable=False)
    registered_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(255), nullable=False)
    posts   = db.relationship("Post", backref="author", lazy=True, cascade="all, delete")
    comments = db.relationship("Comment", backref="commenter", lazy=True)
    
    def __repr__(self)->str:
        return f"User(user_id = {self.user_id}, username = {self.username})"
class Post(db.Model):
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caption = db.Column(db.String(255), default="")
    image_uri = db.Column(db.String(255), default=None)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    comments = db.relationship("Comment", backref="aurthor", lazy=True, cascade="all, delete")

    def __repr__(self)->str:
        return f"Post(post_id={self.post_id}, posted_date={self.posted_date})"

class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(200), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __repr__(self)->str:
        return f"Comment(comment_id={self.comment_id}, post_id={self.post_id})"
