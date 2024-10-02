from db import db  # Importer db depuis db.py

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(128), nullable=False)
    profile_picture_url = db.Column(db.String(200), nullable=True)  # New column for avatar URL

    stories = db.relationship('Story', backref='author', lazy=True)

class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    comments = db.relationship('Comment', backref='story', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Nouvelle relation pour accéder à l'auteur du commentaire
    user = db.relationship('User', backref='comments', lazy=True)
