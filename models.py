"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    '''Connect to database. '''

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''Table of users'''

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    img_url = db.Column(db.Text,
                        nullable=False,
                        default='/static/power-symbol-variant.svg')

    def __repr__(self):

        return f'''<User {self.id} {self.first_name}
         {self.last_name} {self.img_url}>'''


class Post(db.Model):
    ''' Table of user posts '''

    __tablename__ = 'posts'

    user = db.relationship('User', backref='posts')

    posts_tags = db.relationship('PostTag', backref='posts')

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           default=datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    def __repr__(self):

        return f'''<Post {self.id} {self.title} {self.created_at}>'''


class Tag(db.Model):
    ''' Tanle of blog tags '''

    __tablename__ = "tags"

    posts_tags = db.relationship('PostTag', backref='tags')

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(20),
                     unique=True,
                     nullable=False)


class PostTag(db.Model):
    ''' Table of associated posts and tags '''

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
