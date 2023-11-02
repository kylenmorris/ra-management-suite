from RAManagementSuite import db
from enum import Enum

class UserRole(Enum):
    COORDINATOR = "coordinator"
    SENIOR = "senior"
    RETURNER = "returner"
    BASIC = "basic"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.Enum(UserRole), default=UserRole.BASIC, nullable=False)

