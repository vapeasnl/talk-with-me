from db import db
from datetime import datetime

# Model User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture_url = db.Column(db.String(200), nullable=True)  # New field

    # Relations
    stories = db.relationship('Story', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    actions = db.relationship('UserAction', backref='user', lazy=True)

# Model Story
class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)  # Add likes attribute
    dislikes = db.Column(db.Integer, default=0)  # Add dislikes attribute

    # Relations
    story_actions = db.relationship('UserAction', backref='acted_on_story', lazy=True, cascade="all, delete-orphan")

# Model Comment
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)  # Add likes attribute
    dislikes = db.Column(db.Integer, default=0)  # Add dislikes attribute

    # Add the relationship to User
    user = db.relationship('User', backref='comments_by_user')
    comment_actions = db.relationship('UserAction', backref='related_comment_action', lazy=True, cascade="all, delete-orphan")


# Model UserAction
class UserAction(db.Model):
    __tablename__ = 'user_action'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    liked = db.Column(db.Boolean, default=False)
    disliked = db.Column(db.Boolean, default=False)

    # Relations
    comment = db.relationship('Comment', backref='user_actions_on_comment', overlaps="comment_actions")
    story = db.relationship('Story', backref='user_actions_on_story')
