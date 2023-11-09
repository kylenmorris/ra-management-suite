from models import User, UserRole
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(email, name, password):
    hashed_password = generate_password_hash(password)
    user = User(email=email, name=name, password=hashed_password)
    db.session.add(user)
    db.session.commit()

# Additional user operations can go here...


def get_all_users():
    return User.query.all()

