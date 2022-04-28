from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), unique=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    title = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state = db.Column(db.Boolean)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), default='No title')
    start = db.Column(db.DateTime(timezone=True), default=func.now())
    end = db.Column(db.DateTime(timezone=True), default=func.now())
    repeat = db.Column(db.Integer, default=0)
    repeat_till = db.Column(db.DateTime(timezone=True), default=func.now())
    color = db.Column(db.String(7), default='#d4d4d4')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(100))
    users = db.relationship('User')
    notes = db.relationship('Note')
    items = db.relationship('Item')
    events = db.relationship('Event')

    def change_group_name(self, new_group_name):
        self.name = new_group_name
        return


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    events = db.relationship('Event')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def change_name(self, new_name):
        self.first_name = new_name

    def change_email(self, new_email):
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        else:
            self.email = new_email
            return True

    def change_password(self, new_password):
        self.password = generate_password_hash(new_password, method='sha256')

