from models import SignupCode
from extensions import db
from random import randint
from werkzeug.exceptions import abort


def get_signup_code(signup_code):
    code = SignupCode.query.filter_by(code=signup_code).first()
    return code


def get_signup_codes():
    return SignupCode.query.all()


def create_signup_code():
    unique = False
    # we need a new code that's unique
    # Try creating new ones until we get one that doesn't exist
    while not unique:
        new_code = randint(100000, 999999)
        existing_code = get_signup_code(new_code)
        if not existing_code:
            unique = True

    code = SignupCode(code=new_code)
    db.session.add(code)
    db.session.commit()


def edit_signup_code(id, used):
    code = SignupCode.query.filter_by(id=id).first()
    if code:
        code.used = used
        db.session.commit()


def delete_signup_code(id):
    try:
        code = SignupCode.query.get(id)
        if code:
            db.session.delete(code)
            db.session.commit()
            return True  # Return a success indicator
        else:
            return False  # Return a failure indicator (announcement not found)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db.session.rollback()
        return False  # Return a failure indicator





