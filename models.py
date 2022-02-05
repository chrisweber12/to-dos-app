from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Contains SQLAlchemy table models
# Chris Weber

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, index=True)
    firstName = db.Column(db.String(50), index=True)
    lastName = db.Column(db.String(50), index=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    # toDos = db.relationship('ToDo', cascade = 'all, delete')
    toDos = db.relationship('ToDo', cascade = 'all, delete')


class ToDo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True, index=True)
    priority = db.Column(db.Integer, index=True)
    text = db.Column(db.String(200), index=True)
    dueDate = db.Column(db.Date, index=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
