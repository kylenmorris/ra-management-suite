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


def get_roles_values():
    return [r.value for r in UserRole]


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def change_user_role(user_id, new_role):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(500, "User Not Found")
    if new_role != user.role.value:
        user.role = UserRole(new_role)
        db.session.commit()
    else:
        # should never be triggered
        abort(500, "User Already Has Role")


def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(500, "User Not Found Can't Remove")
    else:
        db.session.delete(user)
        db.session.commit()
