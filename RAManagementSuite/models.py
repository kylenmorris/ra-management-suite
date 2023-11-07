from .extensions import db
from enum import Enum
from datetime import datetime
from flask_login import UserMixin


class UserRole(Enum):
    COORDINATOR = "coordinator"
    SENIOR = "senior"
    RETURNER = "returner"
    BASIC = "basic"


class TaskPriority(Enum):
    LOW = "green"
    MEDIUM = "yellow"
    HIGH = "red"


class TaskStatus(Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in progress"
    NOT_STARTED = "not started"


# Association table for the many-to-many relationship between Tasks and Users
task_assignments = db.Table('task_assignments',
                            db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                            )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    owner = db.relationship('User', backref=db.backref('events', lazy='dynamic'))
    color = db.Column(db.String(7), default="#007BFF")
    description = db.Column(db.Text, nullable=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime(timezone=True), nullable=False)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.NOT_STARTED, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('created_tasks', lazy='dynamic'))
    assigned_users = db.relationship('User', secondary='task_assignments',
                                     backref=db.backref('assigned_tasks', lazy='dynamic'))
