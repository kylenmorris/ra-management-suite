from extensions import db
from enum import Enum
from datetime import datetime
from flask_login import UserMixin


class UserRole(Enum):
    COORDINATOR = "coordinator"
    SENIOR = "senior"
    RETURNER = "returner"
    BASIC = "basic"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    role = db.Column(db.Enum(UserRole), default=UserRole.BASIC, nullable=False)


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.now)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('events', lazy=True))
    color = db.Column(db.String(7), default="#007BFF")
    description = db.Column(db.Text, nullable=True)


# class UserProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50))
#     last_name = db.Column(db.String(50))
#     birthdate = db.Column(db.Date)
#     phone_number = db.Column(db.String(20))
#     pronouns = db.Column(db.String(20))
#     gender = db.Column(db.String(20))
#     major = db.Column(db.String(50))
#     address_line1 = db.Column(db.String(100))
#     address_line2 = db.Column(db.String(100))
#     postalcode = db.Column(db.String(10))
#     city = db.Column(db.String(50))
#     province = db.Column(db.String(50))
#     shift_availability = db.Column(db.String(100))
#     user = db.relationship('User', back_populates='profile')
