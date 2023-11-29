from extensions import db
from enum import Enum
from datetime import datetime
from flask_login import UserMixin


class UserRole(Enum):
    COORDINATOR = "Coordinator"
    SENIOR = "Senior RA"
    RETURNER = "Returned RA"
    BASIC = "RA"


class TaskPriority(Enum):
    LOW = "green"
    MEDIUM = "blue"
    HIGH = "red"


class TaskStatus(Enum):
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    NOT_STARTED = "Not Started"


class EventType(Enum):
    NORMAL = "normal"
    DUTY_SHIFT = "duty shift"


# Association table for the many-to-many relationship between Tasks and Users
task_assignments = db.Table('task_assignments',
                            db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                            )


# class TaskAssignment(db.Model):
#     task_assignment_id = db.Column(db.Integer, primary_key=True)
#     task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('announcements', lazy=True))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User',foreign_keys=[owner_id], backref=db.backref('events', lazy='dynamic'))
    color = db.Column(db.String(7), default="#007BFF")
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.Enum(EventType), default=EventType.NORMAL, nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_user = db.relationship('User', foreign_keys=[assigned_user_id],
                                    backref=db.backref('duty_shifts', lazy='dynamic'))


class SignupCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    created = db.Column(db.DateTime(timezone=True), default=datetime.now)
    used = db.Column(db.Boolean, nullable=False, default=False)
    formatted_created = db.Column(db.String, nullable=True, default="")
    formatted_expires = db.Column(db.String, nullable=True, default="")


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
