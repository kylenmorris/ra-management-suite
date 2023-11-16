from extensions import db
from enum import Enum
from datetime import datetime
from flask_login import UserMixin


class UserRole(Enum):
    COORDINATOR = "Coordinator"
    SENIOR = "Senior RA"
    RETURNER = "Returned RA"
    BASIC = "RA"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
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


class SignupCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.now)
    used = db.Column(db.Boolean, nullable=False, default=False)


class ProfileForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    birthdate = db.Column(db.Date)
    phonenumber = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    pronouns = db.Column(db.String(20))
    major = db.Column(db.String(100))
    addressline1 = db.Column(db.String(255))
    addressline2 = db.Column(db.String(255))
    postcode = db.Column(db.String(20))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    shift_availability = db.Column(db.String(200))
