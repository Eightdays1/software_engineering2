from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    title = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state = db.Column(db.Boolean)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = db.relationship('User')
    notes = db.relationship('Note')
    items = db.relationship('Item')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


