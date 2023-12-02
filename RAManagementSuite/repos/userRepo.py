from models import User, UserRole, Profile
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort


def get_user_by_email(email):
    return User.query.filter_by(email=email, deleted=False).first()



def create_user(email, name, password):
    hashed_password = generate_password_hash(password)
    user = User(email=email, name=name, password=hashed_password)
    db.session.add(user)
    db.session.commit()


def get_all_users():
    return User.query.filter_by(deleted=False)


def get_roles_values():
    return [r.value for r in UserRole]


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id, deleted=False).first()


def change_user_role(user_id, new_role):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(500, "ERROR 500: User Not Found")
    if new_role != user.role.value:
        user.role = UserRole(new_role)
        db.session.commit()
    else:
        # should never be triggered
        abort(500, "User Already Has Role")


def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(500, "ERROR 500: User Not Found Can't Remove")
    else:
        user.role = UserRole.BASIC
        user.deleted = True
        db.session.commit()


def get_user_profile(user_id):
    return Profile.query.filter_by(user_id=user_id).first()


def update_user_profile(user_id, name, phone_number, gender, pronouns, availability):
    profile = Profile.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(id=user_id).first()
    if profile:
        profile.phone_number = phone_number
        profile.gender = gender
        profile.pronouns = pronouns
        profile.availability = availability
        user.name = name
        db.session.commit()
    else:
        # Create a new profile if it doesn't exist
        new_profile = Profile(user_id=user_id, phone_number=phone_number, gender=gender, pronouns=pronouns,
                              availability=availability)
        db.session.add(new_profile)
        db.session.commit()